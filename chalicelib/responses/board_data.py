from collections import OrderedDict
from itertools import combinations, product
from datetime import datetime


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

        # # Feedback (Validation)
        # for semester, data in self.board_data.items():
        #     self.board_data[semester]["feedback"] = self.feedback_data(data)

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

    def validate(self):
        ret = {}
        for semester, data in self.board_data.items():
            ret[semester] = self.feedback_data(data)
        return ret

    @staticmethod
    def feedback_data(data):
        def validate_time():
            overlap_msg = "%s and %s class times are overlapped."
            feedback = {"type": "time", "ok": True, "reason": ""}

            def is_time_overlap(a, b):
                class_time_format = "%H:%M"
                _, day_a, start_a, end_a = tuple(a.split(", "))
                _, day_b, start_b, end_b = tuple(b.split(", "))
                if day_a != day_b:
                    return False
                start_a = datetime.strptime(start_a[:4], class_time_format)
                end_a = datetime.strptime(end_a[:4], class_time_format)
                start_b = datetime.strptime(start_b[:4], class_time_format)
                end_b = datetime.strptime(end_b[:4], class_time_format)
                assert start_a < end_a and start_b < end_b
                return False if end_a < start_b or end_b < start_a else True

            courses = data["courses"]
            pair = combinations(courses, 2)
            for a, b in pair:
                time_a = None  # [[Class | Lab, Day, From, To]]
                time_b = None
                # Find lecture time
                for lecture in a["lectures"]:
                    if lecture["division"] == a["selectedDivision"]:
                        time_a = lecture["classTime"]
                for lecture in b["lectures"]:
                    if lecture["division"] == b["selectedDivision"]:
                        time_b = lecture["classTime"]

                # 아직 분반을 선택하지 않음
                if time_a is None or time_b is None:
                    continue

                # Is conflict?
                conflict = False
                for x, y in product(time_a, time_b):
                    if is_time_overlap(x, y):
                        conflict = True
                if conflict:
                    feedback["ok"] = False
                    feedback["reason"] += overlap_msg % (a["courseNumber"], b["courseNumber"])

            return feedback

        def validate_prerequisite():
            return {
                "type": "prerequisite",  # prerequisite | time
                "ok": True,
                "reason": "You are always okay."
            }

        return [validate_time(), validate_prerequisite()]

    @property
    def serialize(self):
        return {
            "boardData": self.board_data,
            "currentSemester": self.current_semester
        }
