from chalice import Chalice

from chalicelib.overall import generate_overall
from chalicelib.detail import generate_detail
from chalicelib import pin
from chalicelib.recommendation import recommend

app = Chalice(app_name='cs408e-endpoints')
app.debug = True


# GET: 전체 개설과목 조회
@app.route('/courses/{year}/{term}', cors=True)
def get_all_courses(year, term):
    search_filter = app.current_request.query_params or {}
    return generate_overall(year, term, search_filter)


# GET: 세부 과목 조회
@app.route('/course/{course_number}', cors=True)
def get_specific_course_detail(course_number):
    qs = app.current_request.query_params or {}
    subtitle = qs.pop("subtitle", "")
    return generate_detail(course_number, subtitle)


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


# POST: 과목 추천
@app.route('/recommend', methods=['POST'], cors=True)
def recommend_courses():
    body = app.current_request.json_body
    return recommend(body)


def _get_authorized_student_id(req):
    # TODO: Implement `Login` feature
    return "DUMMY"
