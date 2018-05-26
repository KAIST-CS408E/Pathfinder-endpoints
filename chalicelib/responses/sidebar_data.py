from chalicelib.responses.course_key import CourseKey


class SideBarData:
    def __init__(self, data):
        self.trend = [CourseKey(d).serialize for d in data["trend"]]
        self.new_courses = [CourseKey(d).serialize for d in data["course"]]
        self.new_lectures = [CourseKey(d).serialize for d in data["lecture"]]

    @property
    def serialize(self):
        return {
            "statistics": {
                "trend": self.trend,
                "new": {
                    "courses": self.new_courses,
                    "lectures": self.new_lectures
                }
            }
        }


# {
#     "relevance": {
#         "semester": [
#             {"courseNumber": "CS000", "name": "", "subtitle": ""},
#             {"courseNumber": "CS000", "name": "", "subtitle": ""},
#             {"courseNumber": "CS000", "name": "", "subtitle": ""}
#         ],
#         "history": [
#             {"courseNumber": "CS000", "name": "", "subtitle": ""},
#             {"courseNumber": "CS000", "name": "", "subtitle": ""},
#             {"courseNumber": "CS000", "name": "", "subtitle": ""}
#         ]
#     }
# }
