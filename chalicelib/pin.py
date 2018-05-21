import requests
import json
from . import config

NEO4J_CONFIG = config.NEO4J_CONFIG

QUERY_PINNED_COURSES = """
    MATCH (:Student {studentID: {studentID}})-[:PIN]->(c:Course)
    RETURN c.number, c.name
    ORDER BY c.number
"""

QUERY_PIN_COURSE = """
    MATCH (s:Student {studentID: {studentID}}), (c:Course {number: {number}, subtitle: {subtitle}})
    CREATE UNIQUE (s)-[:PIN]->(c)
"""

QUERY_UNPIN_COURSE = """
    MATCH (:Student {studentID: {studentID}})-[p:PIN]->(:Course {number: {number}, subtitle: {subtitle}})
    DELETE p
"""

NEO4J_URL = "%s:%s/%s/" % (NEO4J_CONFIG["host"], NEO4J_CONFIG["port"], "db/data/cypher")
HEADERS = NEO4J_CONFIG["headers"]
AUTH = (NEO4J_CONFIG["username"], NEO4J_CONFIG["password"])


def get_pinned_courses(student_id):
    params = {"studentID": student_id}
    r = __requests(QUERY_PINNED_COURSES, params)
    return r.json()['data'] if r.json() else []


def change_pinned_status(student_id, course_number, subtitle, is_pin):
    query = QUERY_PIN_COURSE if is_pin else QUERY_UNPIN_COURSE
    params = {
        "studentID": student_id,
        "number": course_number,
        "subtitle": subtitle
    }
    r = __requests(query, params)
    return {"success": r.status_code == 200}


def __requests(query, params):
    body = {"query": query, "params": params}
    r = requests.post(url=NEO4J_URL, data=json.dumps(body), auth=AUTH, headers=HEADERS)
    assert r.status_code == 200
    return r
