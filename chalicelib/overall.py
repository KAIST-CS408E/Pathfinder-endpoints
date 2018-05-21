import requests
import json
from . import config

NEO4J_CONFIG = config.NEO4J_CONFIG

QUERY_COURSE = """
    MATCH (c:Course)-[:HELD {{ year: {{year}}, term: {{term}} }}]->(l:Lecture)
    WHERE ({keyword}) AND ({departments}) AND ({course_levels})
    RETURN c.number, c.name, c.subtitle, c.code, l.professor, l.division, l.grades, l.classTime, l.dropChange, l.limit
    ORDER BY c.{sort_order}, l.division
"""

SORT_KEYS = {
    "courseName": "name",
    "courseNumber": "number",
    "grade": "grade",
    "load": "load"
}

NEO4J_URL = "%s:%s/%s/" % (NEO4J_CONFIG["host"], NEO4J_CONFIG["port"], "db/data/cypher")
HEADERS = NEO4J_CONFIG["headers"]
AUTH = (NEO4J_CONFIG["username"], NEO4J_CONFIG["password"])


def generate_overall(year, term, search_filter):
    query = {
        "query": __generate_search_query(search_filter),
        "params": {"year": year, "term": term}
    }

    r = requests.post(url=NEO4J_URL, data=json.dumps(query), headers=HEADERS, auth=AUTH)
    assert r.status_code == 200

    return {"year": year, "term": term, "courses": __generate_body(r.json()['data'])}


def __generate_search_query(search_filter):
    return QUERY_COURSE.format(keyword=__keyword_clause(search_filter.pop("keyword")),
                               departments=__department_clause(search_filter.pop("department")),
                               course_levels=__course_level_clause(search_filter.pop("courseLevel")),
                               sort_order=SORT_KEYS[search_filter.pop("sortOrder")])


def __keyword_clause(keyword):
    clause = "c.name =~ '{keyword}' OR c.number =~ '{keyword}' OR l.professor =~ '{keyword}'"
    regex = '(?i).*%s.*' % keyword
    return clause.format(keyword=regex)


def __department_clause(_departments):
    departments = _departments.split(",")
    sub_clause = "c.number =~ '(?i)%s[0-9]{3}'"
    return " OR ".join([sub_clause % d for d in departments])


def __course_level_clause(_course_levels):
    course_levels = _course_levels.replace("00", "").split(",")
    sub_clause = "c.number =~ '[a-zA-Z]{2,3}%s[0-9]{2}'"
    return " OR ".join([sub_clause % c for c in course_levels])


def __generate_body(data):
    res = []
    for lecture in data:
        info = {
            "professor": lecture[4],
            "division": lecture[5],
            "grades": generate_grade(lecture[6]),
            "classTime": lecture[7],
            "load": generate_load(),
            "limit": lecture[9]
        }

        found = list(filter(lambda x: x["number"] == lecture[0] and x["subtitle"] == lecture[2], res))
        if found:
            idx = res.index(found[0])
            res[idx]["lectures"].append(info)
        else:
            res.append({
                "number": lecture[0],
                "name": lecture[1],
                "subtitle": lecture[2],
                "code": lecture[3],
                "lectures": [info]
            })
    return res


def generate_grade(grade_list):
    # TODO: Dummy function!
    grade = [
        "4.3", "4.0", "3.7", "3.3", "3.0", "2.7",
        "2.3", "2.0", "1.7", "1.3", "1.0", "0.0"
    ]
    grade_list = list(map(lambda s: int(s), grade_list))
    avg = sum(grade_list) / len(grade_list)
    return grade[min(int(avg), 11)]


def generate_load():
    # TODO: Dummy function!
    return "?"
