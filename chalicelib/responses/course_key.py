class CourseKey:

    def __init__(self, data):
        self.number = data[0]
        self.subtitle = data[1]
        self.name = data[2] if len(data) == 3 else None

    def serialize(self, include_name=False):
        ret = {
            "courseNumber": self.number,
            "subtitle": self.subtitle,
        }
        if include_name:
            ret["name"] = self.name
        return ret
