from chalice import Chalice

from chalicelib import board
from chalicelib import pin
from chalicelib import plan
from chalicelib import relevance
from chalicelib import statistics
from chalicelib.detail import generate_detail
from chalicelib.overall import generate_overall
from chalicelib.recommend import recommend

app = Chalice(app_name='cs408e-endpoints')


# GET: 전체 개설과목 조회
@app.route('/courses/{year}/{term}', cors=True)
def get_all_courses(year, term):
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    search_filter = request.query_params or {}
    return generate_overall(year, term, search_filter, student_id)


# GET: 세부 과목 조회
@app.route('/course/{course_number}', cors=True)
def get_specific_course_detail(course_number):
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    qs = request.query_params or {}
    subtitle = qs.pop("subtitle", "")
    return generate_detail(course_number, subtitle, student_id)


# GET: 과목 PIN 리스트 조회
@app.route('/pin', cors=True)
def get_pinned_courses():
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    return pin.get_pinned_courses(student_id)


# POST | DELETE: 과목 PIN 추가 / 제거
@app.route('/pin/{course_number}', methods=['POST', 'DELETE'], cors=True)
def change_pinned_status(course_number):
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    subtitle = (request.query_params or {}).pop("subtitle", "")
    is_pin = (request.method == 'POST')
    return pin.change_pinned_status(student_id, course_number, subtitle, is_pin)


# GET: 칸반 보드 학기별 데이터
@app.route('/board', cors=True)
def get_board():
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    return board.get_board_data(student_id)


# GET: 칸반 보드 학기별 데이터
@app.route('/board/simulate', cors=True)
def get_board():
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    return board.simulate_further_semesters(student_id)


# GET: 과목 추천
@app.route('/board/recommend', cors=True)
def recommend_courses():
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    return recommend(student_id)


# POST | DELETE: 과목 PLAN 추가 / 제거
@app.route('/plan/{course_number}', methods=['POST', 'DELETE'], cors=True)
def change_planned_status(course_number):
    request = app.current_request
    query_params = request.query_params or {}
    student_id = _get_authorized_student_id(request)
    subtitle = query_params.pop("subtitle", "")
    to = int(query_params.pop("to")) if request.method == 'POST' else None
    assert not to or (1 <= to <= 12)
    division = query_params.pop("division", None) if request.method == 'POST' else None

    return plan.change_planned_status(student_id, course_number, subtitle, to, division)


# GET: 현재 학기 개설되는 과목 중 (트랜드), 신설 과목 또는 수업(교수님)
@app.route('/statistics', cors=True)
def get_statistics():
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    return statistics.get_statistics(student_id)


# GET: 다른 학생들이 지금 학기에 듣는 과목 (전필, 전선)
@app.route('/relevance', cors=True)
def get_relevance():
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    return relevance.get_relevance_data(student_id)


# GET: 검색 히스토리 기반 과목 제안
@app.route('/history', cors=True)
def get_area_by_search_history():
    request = app.current_request
    student_id = _get_authorized_student_id(request)
    history = request.headers["cookie"].split(";")[0]
    return relevance.get_recommend_curriculum(student_id, history)


# Helper: 토큰
def _get_authorized_student_id(req):
    # TODO: Implement `Login` feature
    return "SEAN"
