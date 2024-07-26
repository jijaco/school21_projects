import asyncio
import random
from enum import Enum, auto
from random import choice
import requests


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)


counter_actions = {Action.HIGHKICK: Action.HIGHBLOCK, Action.LOWKICK: Action.LOWBLOCK,
                   Action.HIGHBLOCK: Action.LOWKICK, Action.LOWBLOCK: Action.HIGHKICK}


async def fight():
    agent = Agent()
    agent.__aiter__()
    async for action in agent:
        await asyncio.sleep(random.random() / 10)
        if agent.health <= 0:
            print('Neo wins!')
            return
        if action == Action.HIGHBLOCK or action == Action.LOWBLOCK:
            agent.health -= 1
        print('Agent: %s, Neo: %s, Agent Health: %d' %
              (action, counter_actions[action], agent.health))


async def fightmany(n: int):
    agents = [Agent() for _ in range(n)]
    agents = [obj.__aiter__() for obj in agents]

    async def wrapper(agent: Agent, number_of_agent: int):
        async for action in agent:
            await asyncio.sleep(random.random() / 10)
            if agent.health <= 0:
                break
            if action == Action.HIGHBLOCK or action == Action.LOWBLOCK:
                agent.health -= 1
            print('Agent %d: %s, Neo: %s, Agent Health: %d' %
                  (number_of_agent + 1, action, counter_actions[action], agent.health))
    await asyncio.gather(*[wrapper(agent, index) for agent, index in zip(agents, range(n))])
    print('Neo wins!')

asyncio.run(fight())
n = 3
asyncio.run(fightmany(n))
