from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_PIN_COURSE, QUERY_UNPIN_COURSE, QUERY_PINNED_COURSES


def get_pinned_courses(student_id):
    r = gather_responses(student_id, {"all": QUERY_PINNED_COURSES}, {})
    return r["all"]


def change_pinned_status(student_id, course_number, subtitle, is_pin):
    query = QUERY_PIN_COURSE if is_pin else QUERY_UNPIN_COURSE
    params = {"number": course_number, "subtitle": subtitle}
    res = gather_responses(student_id, {"result": query}, params)
    return {"success": (len(res["result"]) != 0)}
