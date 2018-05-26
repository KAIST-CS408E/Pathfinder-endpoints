import json
from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_COLLABORATIVE_FILTERING, QUERY_TAKE_COURSES

RECOMMENDATION_QUERIES = {
    "recommend": QUERY_COLLABORATIVE_FILTERING,
    "taken": QUERY_TAKE_COURSES
}


def recommend(student_id):
    res = gather_responses(student_id, RECOMMENDATION_QUERIES, {"type": "Major Elective"})
    recommended_area = curriculum(res["taken"])
    return {"area": recommended_area, "cf": res["recommend"]}


def curriculum(taken_courses):
    def __get_course_numbers(courses):
        return list(map(lambda e: e[0], filter(lambda e: e[2] == "Major Elective", courses)))

    def __get_special_topics(courses):
        return list(map(lambda e: e[1], filter(lambda e: e[2] == "Major Elective", courses)))

    match = {}
    score = {}
    with open("chalicelib/helpers/curriculum.json", mode="r") as f:
        areas = json.load(f)
        current_match = 0
        for area, value in areas.items():
            match_point = 0
            # 일반 과목
            taken_course_numbers = __get_course_numbers(taken_courses)
            for course_number in value["curriculum"]:
                if course_number in taken_course_numbers:
                    course_level = int(course_number[-3])
                    match_point += course_level
            # 특강
            taken_special_topics = __get_special_topics(taken_courses)
            for special_topic in value.get("underGraduatedSpecialTopics", []):
                if special_topic in taken_special_topics:
                    match_point += 4

            if current_match < match_point:
                current_match = match_point
                match = {area: value}

            score[area] = match_point
    return match
