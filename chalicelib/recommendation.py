from aiohttp import ClientSession, BasicAuth
import asyncio
import json
from datetime import datetime
from . import config

NEO4J_CONFIG = config.NEO4J_CONFIG

QUERY_TAKE_COURSES = """
    MATCH (:Student {studentID: {studentID}})-[t:TAKE]->(c:Course)
    RETURN t, c
    ORDER BY t.semester, c.number
"""

QUERIES = {
    "courses": QUERY_TAKE_COURSES,
}


def recommend(body):
    student_id = body["studentID"]
    return __gather_detail_information(student_id)


def __gather_detail_information(student_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.Future()
    _ = asyncio.ensure_future(__requests(student_id, future))
    loop.run_until_complete(future)
    return {k: v for d in future.result() for k, v in d.items()}


async def __requests(student_id, future):
    url = "%s:%s/db/data/cypher" % (NEO4J_CONFIG["host"], NEO4J_CONFIG["port"])
    auth = BasicAuth(NEO4J_CONFIG["username"], NEO4J_CONFIG["password"])
    tasks = []

    async with ClientSession(auth=auth, headers=NEO4J_CONFIG["headers"]) as session:
        for key, query in QUERIES.items():
            body = {
                "query": query,
                "params": {
                    "studentID": student_id
                }
            }
            t = asyncio.ensure_future(__fetch(url, key, body, session))
            tasks.append(t)
        responses = await asyncio.gather(*tasks)
        future.set_result(responses)


async def __fetch(url, key, body, session):
    async with session.post(url=url, data=json.dumps(body)) as response:
        value = await response.json()
        return {key: value["data"]}
