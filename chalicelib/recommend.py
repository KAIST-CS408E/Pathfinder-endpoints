from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_TAKE_COURSES

RECOMMENDATION_QUERIES = {
    "courses": QUERY_TAKE_COURSES,
}


def recommend(student_id, body):
    return gather_responses(student_id, RECOMMENDATION_QUERIES, {})
