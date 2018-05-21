from chalice import Chalice
from chalicelib.overall import generate_overall
from chalicelib.detail import generate_detail

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


# POST: 추천
@app.route('/recommend', cors=True)
def recommend_courses():
    return {}
