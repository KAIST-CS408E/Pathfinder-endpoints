from chalicelib.responses.board_data import BoardData
from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_COURSES_IN_BOARD

BOARD_QUERIES = {
    "board": QUERY_COURSES_IN_BOARD
}


def get_board_data(student_id):
    res = gather_responses(student_id, BOARD_QUERIES)
    return BoardData(res["board"]).serialize
