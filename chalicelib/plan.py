from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_PLAN_COURSE, QUERY_UNPLAN_COURSE


def change_planned_status(student_id, course_number, subtitle, to):
    query = QUERY_PLAN_COURSE if to else QUERY_UNPLAN_COURSE
    params = {"number": course_number, "subtitle": subtitle, "to": to}
    res = gather_responses(student_id, {"result": query}, params)

    return {"success": (len(res["result"]) != 0)}
