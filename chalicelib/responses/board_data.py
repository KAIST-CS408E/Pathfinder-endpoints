from collections import OrderedDict


class BoardData:
    board_data = None
    current_semester = 0

    def __init__(self, data):
        self.board_data = OrderedDict()
        # Create Data
        for d in data:
            rel_type = d[0]
            semester = d[1]
            division = d[2]
            grade = d[3]
            course = d[4]["data"]
            lectures = [l["data"] for l in d[5]]

            if semester not in self.board_data.keys():
                self.board_data[semester] = {"courses": [], "feedback": []}

            self.board_data[semester]["courses"].append(self.course_data(course, rel_type, division, grade, lectures))
            if rel_type == 'TAKE':
                self.current_semester = max(semester, self.current_semester)

        # Feedback (Validation)
        for semester in self.board_data.keys():
            self.board_data[semester]["feedback"].append(self.feedback_data())

    @staticmethod
    def course_data(course, rel_type, division, grade, lectures):
        def __lecture_data(lecture):
            key = ["professor", "division", "classTime", "limit", "abandonmentRate"]
            ret = OrderedDict()
            for k in key:
                ret[k] = lecture.get(k)
            ret["load"] = lecture.get("spendTime", "< 1")
            ret["grades"] = lecture.get("averageGrade", "0.0")
            return ret

        key = ["name", "subtitle"]
        data = OrderedDict()
        for k in key:
            data[k] = course.get(k)
        data["courseNumber"] = course["number"]
        data["courseType"] = course["type"]
        data["type"] = rel_type  # TODO
        data["lectures"] = [__lecture_data(l) for l in lectures]
        data["selectedDivision"] = division
        data["myGrade"] = grade
        return data

    @staticmethod
    def feedback_data():
        def validation_time(self):
            pass

        def validation_prerequisite(self):
            pass

        return {
            "type": "prerequisite",  # prerequisite | time
            "ok": True,
            "reason": "You are always okay."
        }

    @property
    def serialize(self):
        import pprint
        pprint.pprint(self.board_data)
        return {
            "boardData": self.board_data,
            "currentSemester": self.current_semester
        }
