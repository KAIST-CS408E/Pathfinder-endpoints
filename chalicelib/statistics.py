from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_NEW_COURSE_OR_LECTURE


def get_statistics(student_id):
    ret = []
    key = ["courseNumber", "subtitle", "name", "professor", "isNewCourse"]

    res = gather_responses(student_id, {"new": QUERY_NEW_COURSE_OR_LECTURE})
    new_lectures = res["new"]
    for n in new_lectures:
        o = {}
        for idx, k in enumerate(key):
            o[k] = n[idx]
        ret.append(o)

    return ret
