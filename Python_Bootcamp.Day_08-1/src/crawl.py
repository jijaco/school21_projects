import asyncio
import aiohttp
from time import time
from server import UrlsList

host = "http://localhost:8888/api/v1/tasks"


async def post_request(session, urls: list):
    urls = list(set(urls))
    data = UrlsList(urls=urls)
    header = {'Content-Type': 'application/json'}
    async with session.post(url=host, data=data.model_dump_json(), headers=header) as response:
        print(response.status)


async def get_uuid(session):
    async with session.get(url=host) as response:
        uuid = await response.json()
        return uuid


async def get_request(session, uuid):
    async with session.get(url=host + '/' + uuid) as req:
        response = await req.json()
        for key in response:
            print(f'{response[key]}\t {key}')


async def main(urls: list):
    async with aiohttp.ClientSession() as session:
        await post_request(session, urls)
        uuid = await get_uuid(session)
        await get_request(session, uuid)


if __name__ == '__main__':
    list_urls = ["https://www.baidu.com",
                 "https://www.google.com",
                 "https://www.google.com/search?q=there+is+no+spoon",
                 "https://www.yahoo.com",
                 "https://www.facebook.com",
                 "https://www.ya.ru",
                 "https://www.instagram.com",
                 "https://www.reddit.com"
                 ]
    asyncio.run(main(urls=list_urls))
