from chalice import Chalice
import requests
from chalicelib import config
from chalicelib.helpers.helper import *
from chalicelib.detail import generate_detail

NEO4J_CONFIG = config.NEO4J_CONFIG

NEO4J_URL = "%s:%s/%s/" % (NEO4J_CONFIG["host"], NEO4J_CONFIG["port"], "db/data/cypher")
HEADERS = NEO4J_CONFIG["headers"]
AUTH = (NEO4J_CONFIG["username"], NEO4J_CONFIG["password"])

app = Chalice(app_name='cs408e-endpoints')
app.debug = True


# GET: 전체 개설과목 조회
@app.route('/courses/{year}/{term}', cors=True)
def get_all_courses(year, term):
    search_filter = app.current_request.query_params or {}
    query = {
        "query": generate_search_query(search_filter),
        "params": {"year": year, "term": term}
    }

    r = requests.post(url=NEO4J_URL, data=json.dumps(query), headers=HEADERS, auth=AUTH)
    assert r.status_code == 200

    return {"year": year, "term": term, "courses": generate_body(r.json()['data'])}


# GET: 세부 과목 조회
@app.route('/course/{course_no}', cors=True)
def get_specific_course_detail(course_no):
    return generate_detail(course_no)
