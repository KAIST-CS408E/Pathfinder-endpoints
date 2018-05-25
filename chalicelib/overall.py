from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_ALL_COURSES, QUERY_TAKE_COURSES_THIS_TIME, QUERY_PINNED_COURSES_THIS_TIME


def generate_overall(year, term, search_filter, student_id):
    queries = {
        "all": __generate_search_query(search_filter),
        "take": QUERY_TAKE_COURSES_THIS_TIME,
        "pinned": QUERY_PINNED_COURSES_THIS_TIME
    }
    params = {"year": int(year), "term": term}
    res = gather_responses(student_id, queries, params)

    return {
        "year": year,
        "term": term,
        "courses": __generate_body(res["all"]),
        "pinned": res["pinned"],
        "take": res["take"]
    }

    # 다음 학기 (2018 가을)
    # 이번 학기 (2018 봄)
    #
    # averageGrade가 없는 수업은 최신 수업 (2018년 봄, 가을 전부)
    # abandonmentRate가 없는 수업은 최신 수업 (2018년 가을) (위의 부분집합)


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
        course_levels.sort(key=lambda e: int(e))
        if '5' == course_levels[-1]:
            course_levels[-1] = '[5-9]'
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
    res = []
    for lecture in data:
        info = {
            "professor": lecture[4],
            "division": lecture[5],
            "grades": lecture[6],
            "classTime": lecture[7],
            "load": lecture[8],
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
