from datetime import datetime

# 개설 과목
QUERY_ALL_COURSES = """
    MATCH (c:Course)-[:HELD {{ year: {{year}}, term: {{term}} }}]->(l:Lecture)
    WHERE ({keyword}) AND ({departments}) AND ({course_levels})
    RETURN c.number, c.name, c.subtitle, c.code, l.professor, l.division, l.grades, l.classTime, l.dropChange, l.limit
    ORDER BY c.{sort_order}, l.division
"""

# 현재 학기에 개설된 과목 중 핀 한 과목
QUERY_PINNED_COURSES_THIS_TIME = """
    MATCH (:Student {studentID: {studentID}})-[:PIN]->(c:Course)-[:HELD {year: {year}, term: {term}}]->(:Lecture)
    RETURN c.number, c.subtitle
    ORDER BY c.number
"""


# 과목 디테일
QUERY_ABOUT_THIS_COURSE = """
    MATCH (c:Course {number: {courseNumber}, subtitle: {subtitle}})-[h:HELD]->(l:Lecture)
    WHERE %s - toInt(h.year) < 5
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
""" % datetime.now().year

# 같이 듣는 과목
QUERY_WITH_THIS_COURSE = """
    MATCH (:Course {number: {courseNumber}, subtitle: {subtitle}})<-[t1:TAKE]-(:Student)-[t2:TAKE]->(n:Course)
    WHERE toInt(t1.semester) = toInt(t2.semester)
    RETURN n.number, n.name, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

# 선수 과목들
QUERY_BEFORE_THIS_COURSE = """
    MATCH (n:Course)<-[t1:TAKE]-(:Student)-[t2:TAKE]->(:Course {number: {courseNumber}, subtitle: {subtitle}})
    WHERE toInt(t1.semester) < toInt(t2.semester)
    RETURN n.number, n.name, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

# 직후 과목들
QUERY_AFTER_THIS_COURSE = """
    MATCH (:Course {number: {courseNumber}, subtitle: {subtitle}})<-[t1:TAKE]-(:Student)-[t2:TAKE]->(n:Course)
    WHERE toInt(t1.semester) + 1 = toInt(t2.semester)
    RETURN n.number, n.name, count(*) as cnt
    ORDER BY cnt DESC
    LIMIT 5
"""

# 과목 디테일 쿼리 집합
COURSE_DETAIL_QUERIES = {
    "about": QUERY_ABOUT_THIS_COURSE,
    "before": QUERY_BEFORE_THIS_COURSE,
    "with": QUERY_WITH_THIS_COURSE,
    "after": QUERY_AFTER_THIS_COURSE
}

# 핀 한 과목 전체
QUERY_PINNED_COURSES = """
    MATCH (:Student {studentID: {studentID}})-[:PIN]->(c:Course)
    RETURN c.number, c.name, c.subtitle
    ORDER BY c.number
"""

# 과목 핀
QUERY_PIN_COURSE = """
    MATCH (s:Student {studentID: {studentID}}), (c:Course {number: {number}, subtitle: {subtitle}})
    CREATE UNIQUE (s)-[:PIN]->(c)
"""

# 과목 핀 취소
QUERY_UNPIN_COURSE = """
    MATCH (:Student {studentID: {studentID}})-[p:PIN]->(:Course {number: {number}, subtitle: {subtitle}})
    DELETE p
"""

# 수강한 과목
QUERY_TAKE_COURSES = """
    MATCH (:Student {studentID: {studentID}})-[t:TAKE]->(c:Course)
    RETURN t, c
    ORDER BY t.semester, c.number
"""
