import os

import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException

app = FastAPI()

# from db import create_user, get_user, get_all_users
import db as queries  # ✅ Correct: import the whole module

# ✅ Import your Pydantic models
from schemas import (
    UserCreate,
    UserGet,
    UserPatch,
    UserPut,
    CourseCreate,
    LessonCreate,
    EnrollmentCreate,
    AssignmentCreate,
    SubmissionCreate,
    MessageCreate,
    MessageGet,
    ResourceCreate,
    AttendanceCreate,
)

"""
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""


# INSPIRATION FOR A LIST-ENDPOINT - Not necessary to use pydantic models, but we could to ascertain that we return the correct values
# @app.get("/items/")
# def read_items():
#     con = get_connection()
#     items = get_items(con)
#     return {"items": items}


# INSPIRATION FOR A POST-ENDPOINT, uses a pydantic model to validate
# @app.post("/validation_items/")
# def create_item_validation(item: ItemCreate):
#     con = get_connection()
#     item_id = add_item_validation(con, item)
#     return {"item_id": item_id}


# IMPLEMENT THE ACTUAL ENDPOINTS! Feel free to remove

# -------------------------
# USERS
# -------------------------

@app.post("/users/", status_code=201)
def create_user_route(user: UserCreate):
    con = get_connection()
    try:
        new_user = queries.create_user(con, **user.dict())
        return {"user": new_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}")
def get_user(user_id: int):
    con = get_connection()
    user = queries.get_user(con, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}

@app.get("/users/")
def list_users():
    con = get_connection()
    users = queries.get_all_users(con)
    return {"users": users}

# -------------------------
# COURSES
# -------------------------

@app.post("/courses/", status_code=201)
def create_course(course: CourseCreate):
    con = get_connection()
    try:
        new_course = queries.create_course(con, **course.dict())
        return {"course": new_course}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    con = get_connection()
    course = queries.get_course(con, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"course": course}


@app.get("/teachers/{teacher_id}/courses")
def get_courses_by_teacher(teacher_id: int):
    con = get_connection()
    courses = queries.get_courses_by_teacher(con, teacher_id)
    return {"courses": courses}

# -------------------------
# LESSONS
# -------------------------

@app.post("/lessons/", status_code=201)
def create_lesson(lesson: LessonCreate):
    con = get_connection()
    new_lesson = queries.create_lesson(con, **lesson.dict())
    return {"lesson": new_lesson}


@app.get("/courses/{course_id}/lessons")
def get_lessons(course_id: int):
    con = get_connection()
    lessons = queries.get_lessons_for_course(con, course_id)
    return {"lessons": lessons}

# -------------------------
# ENROLLMENTS
# -------------------------

@app.post("/enrollments/", status_code=201)
def enroll_user(enrollment: EnrollmentCreate):
    con = get_connection()
    try:
        enrollment_row = queries.enroll_user(con, enrollment.user_id, enrollment.course_id)
        return {"enrollment": enrollment_row}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/courses/{course_id}/students")
def get_enrolled_students(course_id: int):
    con = get_connection()
    students = queries.get_enrolled_students(con, course_id)
    return {"students": students}

# -------------------------
# ASSIGNMENTS
# -------------------------

@app.post("/assignments/", status_code=201)
def create_assignment(assignment: AssignmentCreate):
    con = get_connection()
    new_assignment = queries.create_assignment(con, **assignment.dict())
    return {"assignment": new_assignment}

@app.get("/courses/{course_id}/assignments")
def get_assignments(course_id: int):
    con = get_connection()
    assignments = queries.get_assignments_for_course(con, course_id)
    return {"assignments": assignments}

# -------------------------
# SUBMISSIONS
# -------------------------

@app.post("/submissions/", status_code=201)
def submit_assignment(submission: SubmissionCreate):
    con = get_connection()
    new_submission = queries.submit_assignment(con, **submission.dict())
    return {"submission": new_submission}


@app.put("/submissions/{submission_id}/grade")
def grade_submission(submission_id: int, grade_data: GradeUpdate):
    con = get_connection()
    try:
        updated = queries.grade_submission(con, submission_id, grade_data.grade, grade_data.feedback)
        return {"updated_submission": updated}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# MESSAGES
# -------------------------

@app.post("/messages/", status_code=201)
def send_message(message: MessageCreate):
    con = get_connection()
    new_message = queries.send_message(con, **message.dict())
    return {"message": new_message}


@app.get("/messages/{user1}/{user2}")
def get_messages(user1: int, user2: int):
    con = get_connection()
    messages = queries.get_messages_between_users(con, user1, user2)
    return {"messages": messages}

# -------------------------
# RESOURCES
# -------------------------

@app.post("/resources/", status_code=201)
def add_resource(resource: ResourceCreate):
    con = get_connection()
    new_resource = queries.add_resource(con, **resource.dict())
    return {"resource": new_resource}


@app.get("/courses/{course_id}/resources")
def get_resources(course_id: int):
    con = get_connection()
    resources = queries.get_resources_for_course(con, course_id)
    return {"resources": resources}

# -------------------------
# ATTENDANCE
# -------------------------

@app.post("/attendance/", status_code=201)
def record_attendance(att: AttendanceCreate):
    con = get_connection()
    attendance = queries.record_attendance(con, **att.dict())
    return {"attendance": attendance}

@app.get("/lessons/{lesson_id}/attendance")
def get_attendance(lesson_id: int):
    con = get_connection()
    attendance = queries.get_attendance_for_lesson(con, lesson_id)
    return {"attendance": attendance}