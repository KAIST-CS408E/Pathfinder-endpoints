from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_ABOUT_THIS_COURSE, QUERY_BEFORE_THIS_COURSE, \
    QUERY_WITH_THIS_COURSE, QUERY_AFTER_THIS_COURSE


def generate_detail(course_number, subtitle, student_id):
    queries = {
        "about": QUERY_ABOUT_THIS_COURSE,
        "before": QUERY_BEFORE_THIS_COURSE,
        "with": QUERY_WITH_THIS_COURSE,
        "after": QUERY_AFTER_THIS_COURSE
    }
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
