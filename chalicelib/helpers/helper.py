import requests
import json
import random

def generate_match_param(filter):
    param = {}
    for k, v in filter.items():
        if v == "all":
            continue
        param[k] = "{%s}" % k
    return json.dumps(param).replace('"', '') if param else ''

def generate_grade(grade_list):
    #TODO: Dummy function!
    grade = [
        "4.3", "4.0", "3.7", "3.3", "3.0", "2.7",
        "2.3", "2.0", "1.7", "1.3", "1.0", "0.0"
    ]
    grade_list = list(map(lambda s: int(s), grade_list))
    avg = sum(grade_list) / len(grade_list)
    return grade[min(int(avg), 11)]

def generate_load(load_list):
    #TODO: Dummy function!
    return round(random.uniform(0, 4.3), 2)

def generate_body(data, sort_order):
    res = []
    for lecture in data:
        info = {
            "professor": lecture[3],
            "grades": generate_grade(lecture[4]),
            "load": generate_load(lecture[5]),
            "limit": lecture[6],
            "subtitle": lecture[7]
        }

        found = list(filter(lambda x: x["number"] == lecture[1], res))
        if found:
            idx = res.index(found[0])
            res[idx]["lectures"].append(info)
        else:
            res.append({
                "name": lecture[0],
                "number": lecture[1],
                "code": lecture[2],
                "lectures": [info]
            })

    return sorted(res, key=lambda c: c[sort_order])

def fill_major_info(dic, data):
    dic["name"] = data[0]
    dic["code"] = data[1]
    dic["number"] = data[2]
    dic["type"] = "Major Required"
    dic["time"] = [
        ["Mon", "10:30", "11:45", "Class"],
        ["Wed", "10:30", "11:45", "Class"],
        ["Thu", "19:00", "20:45", "Lab"],
    ]
    dic["flow"] = {"Maybe": "We can do it!"}
    dic["friends"] = ["Smile", "Even", "If", "You", "Are", "Sad"]

def random_professor(meaningless):
    professors = ["Seokchan Ahn", "Yejun Kim", "Chansu Park"]
    return professors[random.randrange(0, 3)]

def generate_detail(data):
    ret = {"lectures": {}}
    if not data:
        return ret
        
    fill_major_info(ret, data[0])
    for lecture in data:
        ret["lectures"].setdefault(lecture[5], {})
        # if lecture[5] not in ret["lectures"].keys():

        ret["lectures"][lecture[5]][random_professor(lecture[6])] = {
            "grades": generate_grade(lecture[7]),
            "load": generate_load(lecture[8]),
            "size": lecture[9]
        }
    return ret
