def generate_search_query(search_filter):
    sort_order = {
            'courseName': "name",
            'courseNumber': "number",
            'grade': "grade",
            'load': "load"
        }.pop(search_filter.pop("sortOrder"))
    keyword = search_filter.pop("keyword")

    departments = search_filter.pop("department").split(',')   #CS, EE, HSS
    course_levels = search_filter.pop("courseLevel").replace("00", "").split(',')    #N00 => N

    match_clause = "MATCH (x:Course)-[r:HELD {year: {year}, term: {term}}]->(n:Lecture)"
    keyword_clause = "x.name =~ '(?i).*%s.*' OR n.professor =~'(?i).*%s.*' OR x.number =~'(?i).*%s.*'" % (keyword, keyword, keyword)
    department_clause = " OR ".join(["x.number =~ '(?i)%s[0-9]{3}'" % d for d in departments])
    course_level_clause = " OR ".join(["x.number =~ '(?i)[A-Z]*%s[0-9]{2}'" % l for l in course_levels])
    where_clause = "WHERE (%s) AND (%s) AND (%s)" % (keyword_clause, department_clause, course_level_clause)
    return_clause = "RETURN x.number, x.name, x.subtitle, x.code, n.professor, n.division, n.grades, n.classTime, n.dropChange, n.limit"
    order_clause = "ORDER BY x.%s" % sort_order

    return "%s %s %s %s" % (match_clause, where_clause, return_clause, order_clause)


def generate_grade(grade_list):
    # TODO: Dummy function!
    grade = [
        "4.3", "4.0", "3.7", "3.3", "3.0", "2.7",
        "2.3", "2.0", "1.7", "1.3", "1.0", "0.0"
    ]
    grade_list = list(map(lambda s: int(s), grade_list))
    avg = sum(grade_list) / len(grade_list)
    return grade[min(int(avg), 11)]


def generate_load():
    # TODO: Dummy function!
    return "?"


def generate_body(data):
    res = []
    for lecture in data:
        info = {
            "professor": lecture[4],
            "division": lecture[5],
            "grades": generate_grade(lecture[6]),
            "classTime": lecture[7],
            "load": generate_load(),
            "limit": lecture[9]
        }

        found = list(filter(lambda x: x["number"] == lecture[0] and x["subtitle"] == lecture[2], res))
        if found:
            idx = res.index(found[0])
            res[idx]["lectures"].append(info)
        else:
            res.append({
                "number": lecture[0] if not lecture[2] else lecture[0] + lecture[5].upper(),
                "name": lecture[1],
                "subtitle": lecture[2],
                "code": lecture[3],
                "lectures": [info]
            })
    return res
