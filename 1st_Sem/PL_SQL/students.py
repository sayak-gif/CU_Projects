# students.py
from db import get_cursor

def add_student(roll_no, name, department, year):
    with get_cursor(commit=True) as cur:
        sql = "INSERT INTO students (roll_no, name, department, year) VALUES (%s,%s,%s,%s)"
        cur.execute(sql, (roll_no, name, department, year))
        print("Student added, id:", cur.lastrowid)

def list_students():
    with get_cursor() as cur:
        cur.execute("SELECT * FROM students ORDER BY student_id")
        for r in cur.fetchall():
            print(r)
