from chalicelib.responses.board_data import BoardData
from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_COURSES_IN_BOARD, QUERY_FURTHER_COURSES_IN_BOARD


def get_board_data(student_id):
    res = gather_responses(student_id, {"board": QUERY_COURSES_IN_BOARD})
    return BoardData(res["board"]).serialize


def simulate_further_semesters(student_id):
    res = gather_responses(student_id, {"further": QUERY_FURTHER_COURSES_IN_BOARD})
    return BoardData(res["further"]).validate()
