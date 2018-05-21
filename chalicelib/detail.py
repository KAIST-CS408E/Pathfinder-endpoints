from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import COURSE_DETAIL_QUERIES


def generate_detail(course_number, subtitle, student_id):
    queries = COURSE_DETAIL_QUERIES
    params = {"courseNumber": course_number, "subtitle": subtitle}
    res = gather_responses(student_id, queries, params)

    about = res.pop("about")
    if not about:
        return {}

    ret = dict(**{"course": {}, "lectures": []}, **res)
    for cl in about:
        course, lecture = cl
        if not ret["course"]:
            ret["course"] = course["data"]
        ret["lectures"].append(lecture["data"])

    return ret
