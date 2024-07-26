from fastapi import FastAPI, HTTPException
from uuid import uuid4
from pydantic import BaseModel, UUID4
from typing import List, Dict
import logging
import asyncio
import aiohttp
import redis.asyncio as aioredis
import uvicorn


class UrlsList(BaseModel):
    urls: List[str]


class Task(BaseModel):
    id: UUID4
    status: str
    result: Dict[str, str]


data = UrlsList(urls=[])
tasks: List[Task] = []


app = FastAPI()

red = aioredis.Redis()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_cache(r: aioredis.Redis):
    pass


async def send_request(url: str):
    value = await red.get(url)
    if value is not None:
        return url, value

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as resp:
                logger.info(f"Receiving text from {url}")
                await resp.text()
                logger.info(f"Received text from {url}")
                return url, resp.status
        except asyncio.TimeoutError:
            logger.error(f"TimeoutError fetching {url}")
            return url, 504
        except Exception as e:
            logger.error(f"Unknown error fetching {url}: {e}")
            return url, 500


@app.post("/api/v1/tasks", status_code=201)
async def receive_url(request: UrlsList):
    task = Task(id=uuid4(), status='', result={})
    tasks.append(task)
    data.urls = request.urls
    return task


@app.get("/api/v1/tasks")
async def send_uuid():
    return tasks[-1].id


@app.get("/api/v1/tasks/{received_task_id}")
async def send_status(received_task_id: UUID4):
    task = tasks[0]
    for for_task in tasks:
        if for_task.id == received_task_id:
            for_task.status = "running"
            task = for_task
            break
    if task.status != "running":
        raise HTTPException(status_code=404, detail="Task not found")
    gets = [asyncio.create_task(send_request(url)) for url in data.urls]
    res = await asyncio.gather(*gets)
    task.result = dict(res)
    task.status = "ready"
    url: str
    for url, status in task.result.items():
        await red.set(url, status, ex=30)
        first_domain_index = url.find('/')+2
        last_domain_index = url.find('/', first_domain_index)
        domain = url[first_domain_index:last_domain_index] if last_domain_index != -1 else url[first_domain_index:]
        val = await red.get(domain)
        await red.set(domain, int(val) + 1 if val is not None else 1, ex=30)
    return task.result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
