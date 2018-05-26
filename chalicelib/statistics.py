from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_NEW_COURSE_OR_LECTURE


def get_statistics(student_id):
    res = gather_responses(student_id, {"new": QUERY_NEW_COURSE_OR_LECTURE})
    return res
