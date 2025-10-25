from db import get_cursor

def add_course(code, title, credits):
    with get_cursor(commit=True) as cur:
        sql = "INSERT INTO courses (code, title, credits) VALUES (%s,%s,%s)"
        cur.execute(sql, (code, title, credits))
        print("Course added id:", cur.lastrowid)
