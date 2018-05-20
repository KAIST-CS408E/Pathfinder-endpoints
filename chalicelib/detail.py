from aiohttp import ClientSession, BasicAuth
import asyncio
import json
from datetime import datetime
from . import config

NEO4J_CONFIG = config.NEO4J_CONFIG

QUERY_ABOUT_THIS_COURSE = """
    MATCH (c:Course {number: {courseNumber}})-[h:HELD]->(l:Lecture)
    WHERE %s - toInt(h.year) < 5
    WITH c, l,
    CASE l.term
      WHEN 'Spring' THEN 0
      WHEN 'Summer' THEN 1
      WHEN 'Fall'   THEN 2
      WHEN 'Winter' THEN 3
      ELSE 4
    END as termOrder
    RETURN c, l
    ORDER BY l.year DESC, termOrder DESC, l.professor ASC
""" % datetime.now().year

# 같이 듣는 과목
QUERY_WITH_THIS_COURSE = """
    MATCH (:Course {number: {courseNumber}})<-[t1:TAKE]-(:Student)-[t2:TAKE]->(n:Course)
    WHERE toInt(t1.semester) = toInt(t2.semester)
    RETURN n.number, n.name, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

# 선수 과목들
QUERY_BEFORE_THIS_COURSE = """
    MATCH (n:Course)<-[t1:TAKE]-(:Student)-[t2:TAKE]->(:Course {number: {courseNumber}})
    WHERE toInt(t1.semester) < toInt(t2.semester)
    RETURN n.number, n.name, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

# 직후 과목들
QUERY_AFTER_THIS_COURSE = """
    MATCH (:Course {number: {courseNumber}})<-[t1:TAKE]-(:Student)-[t2:TAKE]->(n:Course)
    WHERE toInt(t1.semester) + 1 = toInt(t2.semester)
    RETURN n.number, n.name, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

QUERIES = {
    "about": QUERY_ABOUT_THIS_COURSE,
    "before": QUERY_BEFORE_THIS_COURSE,
    "with": QUERY_WITH_THIS_COURSE,
    "after": QUERY_AFTER_THIS_COURSE
}


def generate_detail(course_number):
    info = __gather_detail_information(course_number)
    about = info.pop("about")
    if not about:
        return {}

    ret = dict(**{"course": {}, "lectures": []}, **info)
    for cl in about:
        course, lecture = cl
        if not ret["course"]:
            ret["course"] = course["data"]
        ret["lectures"].append(lecture["data"])

    return ret


def __gather_detail_information(course_number):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.Future()
    _ = asyncio.ensure_future(__requests(course_number, future))
    loop.run_until_complete(future)
    return {k: v for d in future.result() for k, v in d.items()}


async def __requests(course_number, future):
    url = "%s:%s/db/data/cypher" % (NEO4J_CONFIG["host"], NEO4J_CONFIG["port"])
    auth = BasicAuth(NEO4J_CONFIG["username"], NEO4J_CONFIG["password"])
    tasks = []

    async with ClientSession(auth=auth, headers=NEO4J_CONFIG["headers"]) as session:
        for key, query in QUERIES.items():
            body = {
                "query": query,
                "params": {
                    "courseNumber": course_number
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

