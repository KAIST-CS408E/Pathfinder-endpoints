from collections import OrderedDict


class Planner:
    def __init__(self, data):
        self.ret = OrderedDict()
        self.ret["boardData"] = OrderedDict()
        self.ret["currentSemester"] = None

        for pair in data:
            rel = pair[0]["data"]
            rel_t = pair[0]["metadata"]["type"].upper()
            semester = rel["semester"]
            course = pair[1]["data"]

            bd = self.ret["boardData"]
            if semester not in bd.keys():
                bd[semester] = {
                    "year": rel["year"] if rel_t == "TAKE" else None,
                    "term": rel["term"] if rel_t == "TAKE" else None,
                    "courses": []
                }
            if rel_t == "PLAN" and not self.ret["currentSemester"]:
                self.ret["currentSemester"] = semester - 1

            bd[semester]["courses"].append({
                "name": course["name"],
                "courseNumber": course["number"],
                "subtitle": course["subtitle"],

                "selectedDivision": rel["division"],
                "selectedProfessor": rel["professor"] if rel_t == "PLAN" else None,

                "myGrade": rel["grade"] if rel_t == "TAKE" else None
            })

    @property
    def serialize(self):
        return self.ret
