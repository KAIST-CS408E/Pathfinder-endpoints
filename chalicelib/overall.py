from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_ALL_COURSES, QUERY_PINNED_COURSES_THIS_TIME


def generate_overall(year, term, search_filter, student_id):
    queries = {
        "all": __generate_search_query(search_filter),
        "pinned": QUERY_PINNED_COURSES_THIS_TIME
    }
    params = {"year": year, "term": term}
    res = gather_responses(student_id, queries, params)

    return {
        "year": year,
        "term": term,
        "courses": __generate_body(res["all"]),
        "pinned": res["pinned"]
    }


def __generate_search_query(search_filter):
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

    sort_keys = {
        "courseName": "name",
        "courseNumber": "number",
        "grade": "grade",
        "load": "load"
    }

    return QUERY_ALL_COURSES.format(keyword=__keyword_clause(search_filter.pop("keyword")),
                                    departments=__department_clause(search_filter.pop("department")),
                                    course_levels=__course_level_clause(search_filter.pop("courseLevel")),
                                    sort_order=sort_keys[search_filter.pop("sortOrder")])


def __generate_body(data):
    def __generate_grade(grade_list):
        # TODO: Dummy function!
        grade = [
            "4.3", "4.0", "3.7", "3.3", "3.0", "2.7",
            "2.3", "2.0", "1.7", "1.3", "1.0", "0.0"
        ]
        grade_list = list(map(lambda s: int(s), grade_list))
        avg = sum(grade_list) / len(grade_list)
        return grade[min(int(avg), 11)]

    def __generate_load():
        # TODO: Dummy function!
        return "?"

    res = []
    for lecture in data:
        info = {
            "professor": lecture[4],
            "division": lecture[5],
            "grades": __generate_grade(lecture[6]),
            "classTime": lecture[7],
            "load": __generate_load(),
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
