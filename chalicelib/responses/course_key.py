class CourseKey:
    def __init__(self, data):
        self.number = data[0]
        self.name = data[1]
        self.subtitle = data[2]

    @property
    def serialize(self):
        return {
            "courseNumber": self.number,
            "name": self.name,
            "subtitle": self.subtitle
        }
