from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_SIMILAR_STUDENT_TAKES


def get_relevance_data(student_id):
    res = gather_responses(student_id, {"similar": QUERY_SIMILAR_STUDENT_TAKES})
    return res
