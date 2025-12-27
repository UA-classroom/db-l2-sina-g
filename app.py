import os

import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Importing db.py file structure for use in routes/endpoint
from db import (
    create_user, 
    get_user_by_id, 
    get_all_users, 
    update_user, 
    delete_user, 
    create_course, 
    get_course, 
    get_courses_by_teacher, 
    update_course, 
    delete_course,
    create_enrollment, 
    get_enrollment, 
    get_enrollments_by_user,
    create_assignment, 
    get_assignment, 
    get_assignments_by_course, 
    patch_assignment,
    update_assignment, 
    delete_assignment,
    create_message, 
    get_messages_between_users,
    create_submission, 
    get_submission, 
    get_submissions_by_assignment, 
    get_submissions_by_student,
    update_submission_grade, 
    delete_submission,
    create_lesson, 
    get_lesson, 
    get_lessons_by_course, 
    update_lesson, 
    delete_lesson,
    create_resource, 
    get_resource, 
    get_resources_by_course, 
    get_resources_by_lesson, 
    update_resource, 
    delete_resource,
    create_attendance, 
    get_attendance, 
    get_attendance_by_lesson, 
    get_attendance_by_student, 
    update_attendance, 
    delete_attendance,
)
# Importing Schemas data
from schemas import (
    UserCreate,
    UserGet,
    UserPatch,
    UserPut,
    CourseGet,
    CourseCreate,
    CoursePatch,
    CoursePut,
    EnrollmentGet,
    EnrollmentCreate,
    AssignmentGet,
    AssignmentCreate,
    AssignmentUpdate,
    MessageGet,
    MessageCreate,
    SubmissionGet,
    SubmissionCreate,
    GradeUpdate,
    LessonGet,
    LessonCreate,
    LessonPut,
    ResourceGet,
    ResourceCreate,
    ResourcePut,
    AttendanceGet,
    AttendanceCreate,
    AttendancePut,
)

# USERS / routes
@app.post("/users", status_code=201, response_model=UserGet)
def create_user_route(user: UserCreate):
    con = get_connection()
    try:
        new_user = create_user(
            con,
            user.username,
            user.email,
            user.role,
            user.password
        )
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/users/{user_id}", response_model=UserGet)
def get_user_route(user_id: int):
    con = get_connection()
    user = get_user_by_id(con, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=list[UserGet])
def list_users_route():
    con = get_connection()
    users = get_all_users(con)
    return users
    
@app.put("/users/{user_id}", response_model=UserGet)
def update_user_put_route(user_id: int, user: UserPut):
    con = get_connection()

    if user_id != user.user_id:
        raise HTTPException(status_code=400, detail="ID mismatch")

    try:
        updated = update_user(
            con,
            user_id,
            user.username,
            user.email,
            user.role
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.patch("/users/{user_id}", response_model=UserGet)
def update_user_patch_route(user_id: int, user: UserPatch):
    con = get_connection()

    existing = get_user_by_id(con, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    updated_data = {
        "username": user.username if user.username is not None else existing["username"],
        "email": user.email if user.email is not None else existing["email"],
        "role": user.role if user.role is not None else existing["role"],
    }

    try:
        updated = update_user(
            con,
            user_id,
            updated_data["username"],
            updated_data["email"],
            updated_data["role"]
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}", response_model=UserGet)
def delete_user_route(user_id: int):
    con = get_connection()
    try:
        deleted = delete_user(con, user_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# COURSES
# -------------------------
@app.post("/courses", status_code=201, response_model=CourseGet)
def create_course_route(course: CourseCreate):
    con = get_connection()
    try:
        new_course = create_course(
            con,
            course.title,
            course.description,
            course.teacher_id,
            course.start_date,
            course.end_date
        )
        return new_course
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/courses/{course_id}", response_model=CourseGet)
def get_course_route(course_id: int):
    con = get_connection()
    course = get_course(con, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/teachers/{teacher_id}/courses", response_model=list[CourseGet])
def get_courses_by_teacher_route(teacher_id: int):
    con = get_connection()
    courses = get_courses_by_teacher(con, teacher_id)
    return courses

@app.put("/courses/{course_id}", response_model=CourseGet)
def update_course_put_route(course_id: int, course: CoursePut):
    con = get_connection()

    if course_id != course.course_id:
        raise HTTPException(status_code=400, detail="ID mismatch")

    try:
        updated = update_course(
            con,
            course_id,
            course.title,
            course.description,
            course.teacher_id,
            course.start_date,
            course.end_date
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/courses/{course_id}", response_model=CourseGet)
def update_course_patch_route(course_id: int, course: CoursePatch):
    con = get_connection()

    existing = get_course(con, course_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Course not found")

    updated_data = {
        "title": course.title if course.title is not None else existing["title"],
        "description": course.description if course.description is not None else existing["description"],
        "teacher_id": course.teacher_id if course.teacher_id is not None else existing["teacher_id"],
        "start_date": course.start_date if course.start_date is not None else existing["start_date"],
        "end_date": course.end_date if course.end_date is not None else existing["end_date"],
    }

    try:
        updated = update_course(
            con,
            course_id,
            updated_data["title"],
            updated_data["description"],
            updated_data["teacher_id"],
            updated_data["start_date"],
            updated_data["end_date"]
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/courses/{course_id}", response_model=CourseGet)
def delete_course_route(course_id: int):
    con = get_connection()
    try:
        deleted = delete_course(con, course_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# ENROLLMENTS
# -------------------------
@app.post("/enrollments", status_code=201, response_model=EnrollmentGet)
def enroll_user_route(enrollment: EnrollmentCreate):
    con = get_connection()
    try:
        new_enrollment = create_enrollment(
            con,
            enrollment.user_id,
            enrollment.course_id
        )
        return new_enrollment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/enrollments/{enrollment_id}", response_model=EnrollmentGet)
def get_enrollment_route(enrollment_id: int):
    con = get_connection()
    enrollment = get_enrollment(con, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@app.get("/users/{user_id}/enrollments", response_model=list[EnrollmentGet])
def get_enrollments_by_user_route(user_id: int):
    con = get_connection()
    enrollments = get_enrollments_by_user(con, user_id)
    return enrollments

# -------------------------
# ASSIGNMENTS
# -------------------------
@app.post("/assignments", status_code=201, response_model=AssignmentGet)
def create_assignment_route(assignment: AssignmentCreate):
    con = get_connection()
    try:
        new_assignment = create_assignment(
            con,
            assignment.course_id,
            assignment.title,
            assignment.description,
            assignment.due_date
        )
        return new_assignment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/assignments/{assignment_id}", response_model=AssignmentGet)
def get_assignment_route(assignment_id: int):
    con = get_connection()
    assignment = get_assignment(con, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@app.get("/courses/{course_id}/assignments", response_model=list[AssignmentGet])
def get_assignments_by_course_route(course_id: int):
    con = get_connection()
    assignments = get_assignments_by_course(con, course_id)
    return assignments

@app.put("/assignments/{assignment_id}", response_model=AssignmentGet)
def update_assignment_put_route(assignment_id: int, assignment: AssignmentGet):
    con = get_connection()

    if assignment_id != assignment.assignment_id:
        raise HTTPException(status_code=400, detail="ID mismatch")

    try:
        updated = update_assignment(
            con,
            assignment_id,
            assignment.course_id,
            assignment.title,
            assignment.description,
            assignment.due_date
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/assignments/{assignment_id}", response_model=AssignmentGet)
def update_assignment_patch_route(assignment_id: int, assignment: AssignmentUpdate):
    con = get_connection()

    # Check if assignment exists
    existing = get_assignment(con, assignment_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Only update fields thats needed
    update_fields = assignment.model_dump(exclude_unset=True)

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields found for update")

    try:
        updated = patch_assignment(con, assignment_id, update_fields)
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/assignments/{assignment_id}", response_model=AssignmentGet)
def delete_assignment_route(assignment_id: int):
    con = get_connection()
    try:
        deleted = delete_assignment(con, assignment_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -----------------------------
# MESSAGES
# -----------------------------
@app.post("/messages", status_code=201, response_model=MessageGet)
def send_message_route(message: MessageCreate):
    con = get_connection()
    try:
        new_message = create_message(
            con,
            message.sender_id,
            message.receiver_id,
            message.course_id,
            message.content
        )
        return new_message
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/messages/{user1_id}/{user2_id}", response_model=list[MessageGet])
def get_messages_route(user1_id: int, user2_id: int):
    con = get_connection()
    messages = get_messages_between_users(con, user1_id, user2_id)
    return messages

# -----------------------------
# SUBMISSION
# -----------------------------
@app.post("/submissions", status_code=201, response_model=SubmissionGet)
def submit_assignment_route(submission: SubmissionCreate):
    con = get_connection()
    try:
        new_submission = create_submission(
            con,
            submission.assignment_id,
            submission.student_id,
            submission.url
        )
        return new_submission
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/submissions/{submission_id}", response_model=SubmissionGet)
def get_submission_route(submission_id: int):
    con = get_connection()
    submission = get_submission(con, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission

@app.get("/assignments/{assignment_id}/submissions", response_model=list[SubmissionGet])
def get_submissions_by_assignment_route(assignment_id: int):
    con = get_connection()
    submissions = get_submissions_by_assignment(con, assignment_id)
    return submissions

@app.get("/students/{student_id}/submissions", response_model=list[SubmissionGet])
def get_submissions_by_student_route(student_id: int):
    con = get_connection()
    submissions = get_submissions_by_student(con, student_id)
    return submissions

@app.put("/submissions/{submission_id}/grade", response_model=SubmissionGet)
def grade_submission_route(submission_id: int, grade_data: GradeUpdate):
    con = get_connection()
    try:
        updated = update_submission_grade(
            con,
            submission_id,
            grade_data.grade,
            grade_data.feedback
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/submissions/{submission_id}", response_model=SubmissionGet)
def delete_submission_route(submission_id: int):
    con = get_connection()
    try:
        deleted = delete_submission(con, submission_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# LESSONS
# -------------------------
@app.post("/lessons", status_code=201, response_model=LessonGet)
def create_lesson_route(lesson: LessonCreate):
    con = get_connection()
    try:
        new_lesson = create_lesson(
            con,
            lesson.course_id,
            lesson.title,
            lesson.description,
            lesson.scheduled_at,
            lesson.duration_minutes,
            lesson.location
        )
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/lessons/{lesson_id}", response_model=LessonGet)
def get_lesson_route(lesson_id: int):
    con = get_connection()
    lesson = get_lesson(con, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@app.get("/courses/{course_id}/lessons", response_model=list[LessonGet])
def get_lessons_by_course_route(course_id: int):
    con = get_connection()
    lessons = get_lessons_by_course(con, course_id)
    return lessons

@app.put("/lessons/{lesson_id}", response_model=LessonGet)
def update_lesson_put_route(lesson_id: int, lesson: LessonPut):
    con = get_connection()

    if lesson_id != lesson.id:
        raise HTTPException(status_code=400, detail="ID mismatch")

    try:
        updated = update_lesson(
            con,
            lesson_id,
            lesson.course_id,
            lesson.title,
            lesson.description,
            lesson.scheduled_at,
            lesson.duration_minutes,
            lesson.location
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/lessons/{lesson_id}", response_model=LessonGet)
def delete_lesson_route(lesson_id: int):
    con = get_connection()
    try:
        deleted = delete_lesson(con, lesson_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# RESOURCES
# -------------------------
@app.post("/resources", status_code=201, response_model=ResourceGet)
def create_resource_route(resource: ResourceCreate):
    con = get_connection()
    try:
        new_resource = create_resource(
            con,
            resource.course_id,
            resource.lesson_id,
            resource.title,
            resource.type,
            resource.url
        )
        return new_resource
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/resources/{resource_id}", response_model=ResourceGet)
def get_resource_route(resource_id: int):
    con = get_connection()
    resource = get_resource(con, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@app.get("/courses/{course_id}/resources", response_model=list[ResourceGet])
def get_resources_by_course_route(course_id: int):
    con = get_connection()
    resources = get_resources_by_course(con, course_id)
    return resources

@app.get("/lessons/{lesson_id}/resources", response_model=list[ResourceGet])
def get_resources_by_lesson_route(lesson_id: int):
    con = get_connection()
    resources = get_resources_by_lesson(con, lesson_id)
    return resources

@app.put("/resources/{resource_id}", response_model=ResourceGet)
def update_resource_put_route(resource_id: int, resource: ResourcePut):
    con = get_connection()

    if resource_id != resource.resource_id:
        raise HTTPException(status_code=400, detail="ID mismatch")

    try:
        updated = update_resource(
            con,
            resource_id,
            resource.course_id,
            resource.lesson_id,
            resource.title,
            resource.type,
            resource.url,
            resource.uploaded_at
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/resources/{resource_id}", response_model=ResourceGet)
def delete_resource_route(resource_id: int):
    con = get_connection()
    try:
        deleted = delete_resource(con, resource_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# ATTENDANCE
# -------------------------
@app.post("/attendance", status_code=201, response_model=AttendanceGet)
def record_attendance_route(attendance: AttendanceCreate):
    con = get_connection()
    try:
        new_attendance = create_attendance(
            con,
            attendance.lesson_id,
            attendance.student_id,
            attendance.status,
            attendance.url
        )
        return new_attendance
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/attendance/{attendance_id}", response_model=AttendanceGet)
def get_attendance_route(attendance_id: int):
    con = get_connection()
    attendance = get_attendance(con, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance

@app.get("/lessons/{lesson_id}/attendance", response_model=list[AttendanceGet])
def get_attendance_by_lesson_route(lesson_id: int):
    con = get_connection()
    attendance = get_attendance_by_lesson(con, lesson_id)
    return attendance

@app.get("/students/{student_id}/attendance", response_model=list[AttendanceGet])
def get_attendance_by_student_route(student_id: int):
    con = get_connection()
    attendance = get_attendance_by_student(con, student_id)
    return attendance

@app.put("/attendance/{attendance_id}", response_model=AttendanceGet)
def update_attendance_put_route(attendance_id: int, attendance: AttendancePut):
    con = get_connection()

    if attendance_id != attendance.attendance_id:
        raise HTTPException(status_code=400, detail="ID mismatch")

    try:
        updated = update_attendance(
            con,
            attendance_id,
            attendance.lesson_id,
            attendance.student_id,
            attendance.status,
            attendance.url,
            attendance.recorded_at,
            attendance.uploaded_at
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/attendance/{attendance_id}", response_model=AttendanceGet)
def delete_attendance_route(attendance_id: int):
    con = get_connection()
    try:
        deleted = delete_attendance(con, attendance_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
