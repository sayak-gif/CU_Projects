# app.py
import streamlit as st
import pandas as pd
from db import run_query

st.set_page_config(page_title="Student Result Management", layout="wide")

st.title("🎓 Student Result Management System (SRMS)")

menu = st.sidebar.radio("Navigation", ["Add Student", "Add Course", "Record Marks", "View Students", "View Courses", "View Results"])

# --- Add Student ---
if menu == "Add Student":
    st.header("➕ Add New Student")
    roll = st.text_input("Roll No")
    name = st.text_input("Name")
    dept = st.text_input("Department")
    year = st.number_input("Year", min_value=1, max_value=4, step=1)

    if st.button("Add Student"):
        run_query("INSERT INTO students (roll_no, name, department, year) VALUES (%s,%s,%s,%s)", (roll, name, dept, year))
        st.success(f"✅ Student '{name}' added successfully!")

# --- Add Course ---
elif menu == "Add Course":
    st.header("📘 Add New Course")
    code = st.text_input("Course Code")
    title = st.text_input("Course Title")
    credits = st.number_input("Credits", min_value=1, max_value=6, step=1)
    if st.button("Add Course"):
        run_query("INSERT INTO courses (code, title, credits) VALUES (%s,%s,%s)", (code, title, credits))
        st.success(f"✅ Course '{title}' added successfully!")

# --- Record Marks ---
elif menu == "Record Marks":
    st.header("✍️ Record Marks")
    students = run_query("SELECT * FROM students", fetch=True)
    courses = run_query("SELECT * FROM courses", fetch=True)

    if students.empty or courses.empty:
        st.warning("Please add students and courses first!")
    else:
        s = st.selectbox("Select Student", students["name"])
        c = st.selectbox("Select Course", courses["title"])
        marks = st.slider("Marks", 0, 100, 50)
        exam_date = st.date_input("Exam Date")

        if st.button("Save Record"):
            sid = int(students.loc[students["name"] == s, "student_id"].values[0])
            cid = int(courses.loc[courses["title"] == c, "course_id"].values[0])
            run_query("""
                INSERT INTO marks (student_id, course_id, marks, exam_date)
                VALUES (%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE marks=%s, exam_date=%s
            """, (sid, cid, marks, exam_date, marks, exam_date))
            st.success(f"✅ Marks recorded for {s} in {c}!")

# --- View Students ---
elif menu == "View Students":
    st.header("👩‍🎓 All Students")
    df = run_query("SELECT * FROM students", fetch=True)
    st.dataframe(df)

# --- View Courses ---
elif menu == "View Courses":
    st.header("📚 All Courses")
    df = run_query("SELECT * FROM courses", fetch=True)
    st.dataframe(df)

# --- View Results ---
elif menu == "View Results":
    st.header("📊 Student Results")
    students = run_query("SELECT * FROM students", fetch=True)
    if students.empty:
        st.warning("No students found!")
    else:
        s = st.selectbox("Select Student", students["name"])
        sid = int(students.loc[students["name"] == s, "student_id"].values[0])
        q = """
        SELECT c.code, c.title, c.credits, m.marks,
               ROUND(LEAST(m.marks/10,10),2) AS grade_points
        FROM marks m
        JOIN courses c ON m.course_id = c.course_id
        WHERE m.student_id=%s
        """
        df = run_query(q, (sid,), fetch=True)
        if df.empty:
            st.info("No marks recorded yet.")
        else:
            df["Weighted GP"] = df["grade_points"] * df["credits"]
            st.dataframe(df)
            gpa = df["Weighted GP"].sum() / df["credits"].sum()
            st.success(f"🎯 GPA for {s}: **{round(gpa,2)}**")
