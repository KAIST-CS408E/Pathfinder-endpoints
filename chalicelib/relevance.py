import json
from chalicelib.helpers.request import gather_responses
from chalicelib.helpers.queries import QUERY_SIMILAR_STUDENT_TAKES, QUERY_TAKE_COURSES
from chalicelib.recommend import curriculum


def get_relevance_data(student_id):
    keys = ["courseNumber", "subtitle", "name", "courseType", "count"]
    res = gather_responses(student_id, {"similar": QUERY_SIMILAR_STUDENT_TAKES})
    ret = []
    for r in res["similar"]:
        tmp = {}
        for idx, k in enumerate(keys):
            tmp[k] = r[idx]
        ret.append(tmp)
    return ret


def get_recommend_curriculum(student_id, history):
    # res = gather_responses(student_id, {"take": QUERY_TAKE_COURSES})
    # taken_courses = set(tuple(c) for c in res["take"])
    searched_courses = set(tuple(c) for c in json.loads(history))
    # all_relative_courses = taken_courses.union(searched_courses)
    return curriculum(list(searched_courses), include_required=True)
