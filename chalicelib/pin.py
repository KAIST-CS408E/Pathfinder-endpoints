from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_PIN_COURSE, QUERY_UNPIN_COURSE, QUERY_PINNED_COURSES


def get_pinned_courses(student_id):
    ret = []
    key = ["courseNumber", "name", "subtitle"]
    r = gather_responses(student_id, {"result": QUERY_PINNED_COURSES})
    for pinned in r["result"]:
        res = {}
        for idx, k in enumerate(key):
            res[k] = pinned[idx]
        res["lectures"] = [l["data"] for l in pinned[-1]]
        ret.append(res)
    return ret


def change_pinned_status(student_id, course_number, subtitle, is_pin):
    query = QUERY_PIN_COURSE if is_pin else QUERY_UNPIN_COURSE
    params = {"number": course_number, "subtitle": subtitle}
    res = gather_responses(student_id, {"result": query}, params)
    print(res)
    return {"success": (len(res["result"]) != 0)}
