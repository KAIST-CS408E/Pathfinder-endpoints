import json
from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_TAKE_COURSES, QUERY_COLLABORATIVE_FILTERING

RECOMMENDATION_QUERIES = {
    "courses": QUERY_TAKE_COURSES,
    "recommend": QUERY_COLLABORATIVE_FILTERING
}


def recommend(student_id, body):
    return gather_responses(student_id, RECOMMENDATION_QUERIES, {"type": "Major Elective"})


def validate():
    pass


def path(courses):
    with open("area.json", mode="r") as f:
        areas = json.load(f)
        match = {}
        for area, value in areas.items():
            explanation = value["explanation"]
            curriculum = set(value["curriculum"])
            topics = value.get("underGraduatedSpecialTopics", [])
            match[explanation] = len(curriculum.intersection(courses))

