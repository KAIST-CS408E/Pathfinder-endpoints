from collections import OrderedDict


class Lecture:
    key = ["year", "term", "professor", "division", "classTime", "limit", "abandonmentRate"]

    def __init__(self, data, recent_grade, recent_spend_times):
        self.ret = OrderedDict()
        for k in self.key:
            self.ret[k] = data.get(k, None)
        self.ret["classTime"] = self.__prettify_time(self.ret["classTime"])
        self.ret["load"] = data.get("spendTime", self.__get_median_load(recent_spend_times))
        self.ret["grade"] = data.get("averageGrade", recent_grade)

    @staticmethod
    def __prettify_time(time):
        pretty = []
        for e in time:
            t = e.split(', ')
            pretty.append({
                "timeType": t[0],
                "day": t[1],
                "startTime": t[2][:5],
                "endTime": t[3][:5]
            })
        return pretty

    @staticmethod
    def __get_median_load(lst):
        if not lst:
            return None
        order = ["< 1", "1 to 3", "3 to 5", "5 to 7", "> 7"]
        sorted_lst = sorted(lst, key=lambda e: order.index(e))
        index = len(lst) // 2
        return sorted_lst[index]

    @property
    def serialize(self):
        return self.ret
