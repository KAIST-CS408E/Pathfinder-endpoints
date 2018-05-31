from chalicelib.responses.board_data import BoardData
from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_TAKE_COURSES, \
    QUERY_PLANNED_COURSES_ON_BOARD, QUERY_TAKE_COURSES_ON_BOARD
from chalicelib.responses.planner import Planner


def get_board_data(student_id):
    queries = {
        "take": QUERY_TAKE_COURSES_ON_BOARD,
        "plan": QUERY_PLANNED_COURSES_ON_BOARD
    }
    res = gather_responses(student_id, queries)
    return Planner(res["take"] + res["plan"]).serialize


def simulate_further_semesters(student_id):
    # res = gather_responses(student_id, {"taken": QUERY_TAKE_COURSES, "further": QUERY_VALIDATE_BOARD})
    # return BoardData(res["further"]).validate(res["taken"])
    return None
