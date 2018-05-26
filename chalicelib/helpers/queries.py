from datetime import datetime


def __get_current_year():
    return datetime.now().year


def __get_next_semester():
    # TODO
    return (2018, "Fall")


# 전체 개설 과목
QUERY_ALL_COURSES = """
    MATCH (c:Course)-[:HELD {{ year: {{year}}, term: {{term}} }}]->(l:Lecture)
    WHERE ({keyword}) AND ({departments}) AND ({course_levels})
    RETURN c.number, c.name, c.subtitle, c.code,
           l.professor, l.division, l.averageGrade, l.classTime, l.spendTime, l.limit
    ORDER BY c.{sort_order}, l.division
"""

# 현재 학기에 개설된 과목 중 핀 한 과목
QUERY_PINNED_COURSES_THIS_TIME = """
    MATCH (:Student {studentID: {studentID}})-[:PIN]->(c:Course)-[:HELD {year: {year}, term: {term}}]->(:Lecture)
    WITH DISTINCT c as d
    RETURN d.number, d.subtitle
    ORDER BY d.number
"""

# 현재 학기에 개설된 과목 중 수강 한 과목
QUERY_TAKE_COURSES_THIS_TIME = """
    MATCH (:Student {studentID: {studentID}})-[:TAKE]->(c:Course)-[:HELD {year: {year}, term: {term}}]->(:Lecture)
    WITH DISTINCT c as d
    RETURN d.number, d.subtitle
    ORDER BY d.number
"""

# 과목 디테일
QUERY_ABOUT_THIS_COURSE = """
    MATCH (c:Course {number: {courseNumber}, subtitle: {subtitle}})-[h:HELD]->(l:Lecture)
    WHERE %s - h.year < 5
    WITH c, l,
    CASE l.term
      WHEN 'Spring' THEN 0
      WHEN 'Summer' THEN 1
      WHEN 'Fall'   THEN 2
      WHEN 'Winter' THEN 3
      ELSE 4
    END as termOrder
    RETURN c, l
    ORDER BY l.year DESC, termOrder DESC, l.professor ASC
""" % __get_current_year()

# 정책상 선수/후수 과목
QUERY_REQUISITE_OF_THIS_COURSE = """
    MATCH (:Course {number: {courseNumber}, subtitle: {subtitle}})-[r:PREREQUISITE*]->(c:Course)
    RETURN type(head(r)) as t, c.number, c.name, c.subtitle
    ORDER BY c.number
    UNION
    MATCH (:Course {number: {courseNumber}, subtitle: {subtitle}})-[r:POSTREQUISITE]->(c:Course)
    RETURN type(r) as t, c.number, c.name, c.subtitle
    ORDER BY c.number
"""

# 같이 듣는 과목
QUERY_WITH_THIS_COURSE = """
    MATCH (:Course {number: {courseNumber}, subtitle: {subtitle}})<-[t1:TAKE]-(:Student)-[t2:TAKE]->(n:Course)
    WHERE t1.semester = t2.semester
    RETURN n.number, n.name, n.subtitle, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

# 직전 과목들
QUERY_BEFORE_THIS_COURSE = """
    MATCH (n:Course)<-[t1:TAKE]-(:Student)-[t2:TAKE]->(:Course {number: {courseNumber}, subtitle: {subtitle}})
    WHERE t1.semester = t2.semester + 1
    RETURN n.number, n.name, n.subtitle, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

# 직후 과목들
QUERY_AFTER_THIS_COURSE = """
    MATCH (:Course {number: {courseNumber}, subtitle: {subtitle}})<-[t1:TAKE]-(:Student)-[t2:TAKE]->(n:Course)
    WHERE t1.semester + 1 = t2.semester
    RETURN n.number, n.name, n.subtitle, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

# 핀 한 과목 전체
QUERY_PINNED_COURSES = """
    MATCH (:Student {studentID: {studentID}})-[:PIN]->(c:Course)
    RETURN c.number, c.name, c.subtitle
    ORDER BY c.number
"""

# 과목 핀 설정
QUERY_PIN_COURSE = """
    MATCH (s:Student {studentID: {studentID}})
    WITH s
    MATCH (c:Course {number: {number}, subtitle: {subtitle}})
    WHERE NOT (s)-[:TAKE]->(c)
    CREATE UNIQUE (s)-[:PIN]->(c)
    RETURN s
"""

# 과목 핀 취소
QUERY_UNPIN_COURSE = """
    MATCH (:Student {studentID: {studentID}})-[p:PIN]->(:Course {number: {number}, subtitle: {subtitle}})
    WITH p, ID(p) as i
    DELETE p
    RETURN i
"""

# 수강한 과목
QUERY_TAKE_COURSES = """
    MATCH (:Student {studentID: {studentID}})-[:TAKE]->(c:Course)
    WITH DISTINCT c as d
    RETURN d.number, d.subtitle, d.type
    ORDER BY d.number
"""

# 이후 학기에 수강할 예정인 과목
QUERY_PLANNED_COURSES = """
    MATCH (:Student {studentID: {studentID}})-[p:PLAN]->(c:Course)
    WITH p, c MATCH (c)-[h:HELD]->(l:Lecture)
    WHERE 2018 = h.year AND 'Fall' = h.term
    WITH p, c, l
    ORDER BY l.division
    RETURN p, c, collect(l) as lectures
    ORDER BY p.semester, c.number, c.subtitle
"""

# 커리큘럼 보드에 올라갈 모든 과목
QUERY_COURSES_IN_BOARD = """
    MATCH (:Student {studentID: {studentID}})-[t:TAKE]->(c:Course)
    WITH t, c
    MATCH (c)-[h:HELD]->(l:Lecture)
    WHERE t.year = h.year AND t.term = h.term
    WITH t, c, l
    ORDER BY l.division
    RETURN type(t) as type, t.semester as semester, t.division as division, t.grade as grade, c, collect(l) as lectures
    ORDER BY t.semester, c.number, c.subtitle
    UNION
    MATCH (:Student {studentID: {studentID}})-[p:PLAN]->(c:Course)
    WITH p, c MATCH (c)-[h:HELD]->(l:Lecture)
    WHERE h.year = %d AND h.term = '%s'
    WITH p, c, l
    ORDER BY l.division
    RETURN type(p) as type, p.semester as semester, p.division as division, p.grade as grade, c, collect(l) as lectures
    ORDER BY p.semester, c.number, c.subtitle
""" % __get_next_semester()


# 현재 학기 이후 모든 과목
QUERY_VALIDATE_BOARD = """
    MATCH (s:Student {studentID: {studentID}})-[t:TAKE]->(:Course)
    WITH s, max(t.semester) as current_semester
    MATCH (s)-[t:TAKE]->(c:Course)
    WHERE t.semester = current_semester
    WITH t, c
    MATCH (c)-[h:HELD]->(l:Lecture)
    WHERE t.year = h.year AND t.term = h.term
    WITH t, c, l
    ORDER BY l.division
    WITH type(t) as type, t.semester as semester, t.division as division, t.grade as grade,
           c, collect(l) as lectures
    OPTIONAL MATCH (c)-[:PREREQUISITE*]->(pre:Course)
    RETURN type, semester, division, grade, c, lectures, collect(pre) as prerequisites
    ORDER BY semester, c.number, c.subtitle
    UNION
    MATCH (:Student {studentID: {studentID}})-[p:PLAN]->(c:Course)
    WITH p, c
    MATCH (c)-[h:HELD]->(l:Lecture)
    WHERE h.year = %d AND h.term = '%s'
    WITH p, c, l
    ORDER BY l.division
    WITH type(p) as type, p.semester as semester, p.division as division, p.grade as grade,
           c, collect(l) as lectures
    OPTIONAL MATCH (c)-[:PREREQUISITE*]->(pre:Course)
    RETURN type, semester, division, grade, c, lectures, collect(pre) as prerequisites
    ORDER BY semester, c.number, c.subtitle
""" % __get_next_semester()

# 과목 수강 예정 설정
QUERY_PLAN_COURSE = """
    MATCH (s:Student {studentID: {studentID}})
    WITH s
    MATCH (c:Course {number: {number}, subtitle: {subtitle}})
    WHERE NOT (s)-[:TAKE]->(c)
    MERGE (s)-[p:PLAN]->(c)
    SET p.semester = {to}, p.division = {division}
    RETURN p
"""

# 과목 수강 예정 취소
QUERY_UNPLAN_COURSE = """
    MATCH (s:Student {studentID: {studentID}})
    WITH s
    MATCH (s)-[p:PLAN]->(:Course {number: {number}, subtitle: {subtitle}})
    WITH p, ID(p) as i
    DELETE p
    RETURN i
"""

# 과목 추천 1: Collaborative Filtering
QUERY_COLLABORATIVE_FILTERING = """
    MATCH (s:Student {studentID: {studentID}})-[t:TAKE]->(:Course)
    WITH s, (max(t.semester) - min(t.semester) + 2) as cur
    MATCH (s)-[:TAKE]->(:Course)<-[:TAKE]-()-[t:TAKE]->(other:Course {type: {type}})
    WHERE (NOT (s)-[:TAKE]->(other)) AND t.semester > (cur - 2) AND t.semester < (cur + 2)
    WITH other, other.number as courseNumber, count(*) as cnt
    MATCH (:Student)-[t:TAKE]->(:Course {number: courseNumber})
    WITH other, cnt, round(avg(toInt(t.semester))) as avg
    RETURN other.number, other.name, other.subtitle, avg, cnt
    ORDER BY cnt DESC
"""

# 트렌드한 과목

# 현재 학기에 학생들이 많이 들은 과목

# 새로운 강의, 혹은 새로운 교수님 (1년 내)
QUERY_NEW_COURSE = """
    MATCH (l:Lecture {year: 2018, term: 'Fall'})
    WHERE (NOT (l)-[:PREVIOUS]->()) AND (NOT (l)<-[:WITH]-()-[:PREVIOUS]->())
    RETURN l
"""

QUERY_NEW_LECTURE = """
    MATCH (l:Lecture {year: 2018, term: 'Fall'})
    WHERE (NOT (l)-[:PREVIOUS]->()) AND (NOT (l)<-[:WITH]-()-[:PREVIOUS]->())
    WITH l, collect(l) as coll
    MATCH (p)<-[h0:HELD]-(:Course)-[h1:HELD]->()
    WHERE p IN coll AND (h0.year <> h1.year OR h0.term <> h1.term)
    RETURN l.name, DISTINCT p.name;
"""

# 커리큘럼

# 수강 시기
