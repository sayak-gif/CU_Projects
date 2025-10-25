from db import get_cursor

def record_mark(student_id, course_id, marks, exam_date):
    with get_cursor(commit=True) as cur:
        sql = """INSERT INTO marks (student_id, course_id, marks, exam_date)
                 VALUES (%s,%s,%s,%s)
                 ON DUPLICATE KEY UPDATE marks = VALUES(marks), exam_date = VALUES(exam_date)"""
        cur.execute(sql, (student_id, course_id, marks, exam_date))
        print("Mark recorded.")

def student_transcript(student_id):
    with get_cursor() as cur:
        sql = """
        SELECT s.roll_no, s.name, c.code, c.title, c.credits, m.marks
        FROM marks m
        JOIN students s ON m.student_id = s.student_id
        JOIN courses c ON m.course_id = c.course_id
        WHERE s.student_id = %s
        """
        cur.execute(sql, (student_id,))
        rows = cur.fetchall()
        if not rows:
            print("No records.")
            return

        total_weighted = 0
        total_credits = 0
        for r in rows:
            print(r['code'], r['title'], "marks:", r['marks'], "credits:", r['credits'])
            # example: simple grade point: marks/10 capped at 10
            gp = min(10, r['marks'] / 10.0)
            total_weighted += gp * r['credits']
            total_credits += r['credits']
        gpa = total_weighted / total_credits if total_credits else 0
        print("Estimated GPA:", round(gpa, 2))

def course_average(course_id):
    with get_cursor() as cur:
        cur.execute("SELECT AVG(marks) AS avg_marks FROM marks WHERE course_id=%s", (course_id,))
        print("Average marks:", cur.fetchone()['avg_marks'])

def top_students(limit=5):
    with get_cursor() as cur:
        sql = """
        SELECT s.student_id, s.roll_no, s.name, AVG(m.marks) AS avg_marks
        FROM students s
        JOIN marks m ON s.student_id = m.student_id
        GROUP BY s.student_id
        ORDER BY avg_marks DESC
        LIMIT %s
        """
        cur.execute(sql, (limit,))
        for r in cur.fetchall():
            print(r)

