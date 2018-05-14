from chalice import Chalice
import requests
import json
import random
from chalicelib import config
from chalicelib.helpers.helper import *

NEO4J_CONFIG = config.NEO4J_CONFIG

NEO4J_URL = "%s:%s/%s/" % (NEO4J_CONFIG["host"], NEO4J_CONFIG["port"], "db/data/cypher")
HEADERS = NEO4J_CONFIG["headers"]
AUTH = (NEO4J_CONFIG["username"], NEO4J_CONFIG["password"])

app = Chalice(app_name='cs408e-endpoints')

# GET: 전체 개설과목 조회
@app.route('/courses/{year}/{term}', cors=True)
def get_all_courses(year, term):
    filter = app.current_request.query_params or {}
    sort_order = filter.pop("sortOrder", "number")

    default = "MATCH (x %s)-[r {year: {year}, term: {term}}]->(n) \
               RETURN x.name, x.number, x.code, n.professor, n.grades, n.load, n.limit, n.subtitle"
    query = {
        "query" : default % generate_match_param(filter),
        "params" : dict({"year": year, "term": term}, **filter)
    }

    r = requests.post(url=NEO4J_URL, data=json.dumps(query), headers=HEADERS, auth=AUTH)
    assert r.status_code == 200

    return { "year": year, "term": term, "courses": generate_body(r.json()['data'], sort_order) }

# GET: 세부 과목 조회
@app.route('/course/{course_no}', cors=True)
def get_specific_course_detail(course_no):
    query = {
        "query" : "MATCH (x {number: {number}})-[r]->(n) \
                   RETURN x.name, x.code, x.number, x.type, x.time, \
                          n.name, n.professor, n.grades, n.load, n.size",
        "params" : {"number": course_no}
    }

    r = requests.post(url=NEO4J_URL, data=json.dumps(query), headers=HEADERS, auth=AUTH)
    assert r.status_code == 200

    #TODO: 같이 들은 과목, 그래프 => Redis
    return generate_detail(r.json()['data'])
