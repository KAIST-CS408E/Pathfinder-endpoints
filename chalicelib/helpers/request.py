from aiohttp import ClientSession
import asyncio
import json
from chalicelib.helpers.config import NEO4J_URL, NEO4J_AUTH, NEO4J_HEADERS


def gather_responses(student_id, queries, params=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.Future()
    _params = {} if not params else params
    _ = asyncio.ensure_future(__requests(future, queries, student_id, _params))
    loop.run_until_complete(future)
    return {k: v for d in future.result() for k, v in d.items()}


async def __requests(future, queries, student_id, params):
    tasks = []
    async with ClientSession(auth=NEO4J_AUTH, headers=NEO4J_HEADERS) as session:
        for key, q in queries.items():
            body = {
                "query": q,
                "params": dict(**{"studentID": student_id}, **params)
            }
            t = asyncio.ensure_future(__fetch(NEO4J_URL, key, body, session))
            tasks.append(t)
        responses = await asyncio.gather(*tasks)
        future.set_result(responses)


async def __fetch(url, key, body, session):
    async with session.post(url=url, data=json.dumps(body)) as response:
        value = await response.json()
        return {key: value["data"]}
