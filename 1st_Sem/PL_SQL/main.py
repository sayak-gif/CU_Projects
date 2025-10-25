# main.py
from students import add_student, list_students
from courses import add_course
from marks import record_mark, student_transcript, course_average, top_students

def menu():
    while True:
        print("\n1 Add student\n2 List students\n3 Add course\n4 Record mark\n5 Transcript\n6 Course avg\n7 Top students\n0 Exit")
        ch = input("Choice: ").strip()
        if ch == '1':
            roll = input("roll: "); name = input("name: ")
            dept = input("dept: "); year = int(input("year: "))
            add_student(roll, name, dept, year)
        elif ch == '2':
            list_students()
        elif ch == '3':
            code = input("code: "); title = input("title: "); credits = int(input("credits: "))
            add_course(code, title, credits)
        elif ch == '4':
            sid = int(input("student_id: ")); cid = int(input("course_id: "))
            marks = int(input("marks: ")); ed = input("exam_date (YYYY-MM-DD): ")
            record_mark(sid, cid, marks, ed)
        elif ch == '5':
            sid = int(input("student_id: ")); student_transcript(sid)
        elif ch == '6':
            cid = int(input("course_id: ")); course_average(cid)
        elif ch == '7':
            top_students(int(input("N: ")))
        elif ch == '0':
            break
        else:
            print("Invalid.")

if __name__ == "__main__":
    menu()
