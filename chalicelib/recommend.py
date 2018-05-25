import json
from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_COLLABORATIVE_FILTERING

RECOMMENDATION_QUERIES = {
    "recommend": QUERY_COLLABORATIVE_FILTERING
}


def recommend(student_id):
    res = gather_responses(student_id, RECOMMENDATION_QUERIES, {"type": "Major Elective"})
    return res["recommend"]


def curriculum(courses):
    with open("area.json", mode="r") as f:
        areas = json.load(f)
        match = {}
        for area, value in areas.items():
            explanation = value["explanation"]
            c = set(value["curriculum"])
            topics = value.get("underGraduatedSpecialTopics", [])
            match[explanation] = len(c.intersection(courses))

