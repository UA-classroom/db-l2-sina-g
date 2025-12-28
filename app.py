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

# -------------------------
# USERS / routes
# -------------------------
@app.post(
    "/users", 
    status_code=201, 
    response_model=UserGet,
    summary=" Route to create new user",
    description="Creates a new user in the datbase using: username, email, role, and password.",
    responses={
        201: {"description": "User successfully created"},
        400: {"description": "Invalid input or user already exists"},
    },   
)
def create_user_route(user: UserCreate): # Adding schema UserCreate
    """ 
    Create a new user. 

    This endpoint accepts a `UserCreate` schema and returns the newly created user. 
    """
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
    """
    Retrieve a single user by ID.

    This endpoint fetches a user from the database using the provided `user_id`.
    If the user exists, their data is returned in the `UserGet` response model.
    If no matching user is found, a 404 HTTPException is raised.

    Parameters
    ----------
    user_id : int
        The unique identifier of the user.
    
    Returns
    -------
    UserGet
        Schema of the user.

    Raises
    ------
    HTTPException (404)
        If no user with the given ID exists.

    """
    con = get_connection()
    user = get_user_by_id(con, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=list[UserGet])
def list_users_route():
    """
    Retrieve a list of all users.

    This endpoint queries the database for all existing users and returns
    them as a list serialized using the `UserGet` response model.

    Returns
    -------
    list[UserGet]
        A list of all users stored in the database.
    """
    con = get_connection()
    users = get_all_users(con)
    return users

@app.put("/users/{user_id}", response_model=UserGet)
def update_user_put_route(user_id: int, user: UserPut):
    """
    Update an existing user by ID.

    This endpoint updates a user's information using the data provided in the
    `UserPut` model. The `user_id` in the path must match the `user_id` in the
    request body; otherwise, a 400 error is raised. If the update succeeds, the
    updated user is returned. Any database or validation error results in a
    400 HTTPException.

    Parameters
    ----------
    user_id : int
        The ID of the user to update.
    user : UserPut
        The updated user data, including username, email, and role.

    Returns
    -------
    UserGet
        The updated user object.

    Raises
    ------
    HTTPException (400)
        If the path ID and body ID do not match, or if the update fails.
    """
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
    """
    Partially update an existing user by ID.

    This endpoint allows updating one or more fields of a user without requiring
    the full user object. Only the fields provided in the `UserPatch` model are
    modified; any fields omitted remain unchanged. If the user does not exist,
    a 404 error is returned. Any database or validation error results in a
    400 HTTPException.

    Parameters
    ----------
    user_id : int
        The ID of the user to update.
    user : UserPatch
        A partial user update model where each field is optional.

    Returns
    -------
    UserGet
        The updated user object after applying the partial changes.

    Raises
    ------
    HTTPException (404)
        If the user does not exist.
    HTTPException (400)
        If the update operation fails.
    """
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
    """
    Delete a user by ID.

    This endpoint removes a user from the system using the provided `user_id`.
    If the deletion is successful, the deleted user's data is returned using the
    `UserGet` response model. If the user does not exist or the deletion fails,
    a 404 HTTPException is raised.

    Parameters
    ----------
    user_id : int
        The ID of the user to delete.

    Returns
    -------
    UserGet
        The data of the deleted user.

    Raises
    ------
    HTTPException (404)
        If the user does not exist or the deletion operation fails.
    """
    con = get_connection()
    try:
        deleted = delete_user(con, user_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# COURSES / routes
# -------------------------
@app.post("/courses", status_code=201, response_model=CourseGet)
def create_course_route(course: CourseCreate):
    """
    Create a new course.

    This endpoint creates a new course using the data provided in the
    `CourseCreate` model. If the creation succeeds, the newly created course
    is returned using the `CourseGet` response model. Any validation or
    database error results in a 400 HTTPException.

    Parameters
    ----------
    course : CourseCreate
        The course data including title, description, teacher ID, start date,
        and end date.

    Returns
    -------
    CourseGet
        The newly created course.

    Raises
    ------
    HTTPException (400)
        If the course cannot be created due to invalid data or a database error.
    """
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
    """
    Get a course by ID.

    This endpoint fetches a single course using the provided `course_id`.
    If the course does not exist, a 404 HTTPException is raised. On success,
    the course is returned using the `CourseGet` response model.

    Parameters
    ----------
    course_id : int
        The ID of the course to retrieve.

    Returns
    -------
    CourseGet
        The requested course.

    Raises
    ------
    HTTPException (404)
        If the course does not exist.
    """
    con = get_connection()
    course = get_course(con, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/teachers/{teacher_id}/courses", response_model=list[CourseGet])
def get_courses_by_teacher_route(teacher_id: int):
    """
    Get all courses taught by a specific teacher.

    This endpoint returns a list of courses associated with the given
    `teacher_id`. If the teacher has no courses, an empty list is returned.

    Parameters
    ----------
    teacher_id : int
        The ID of the teacher whose courses should be retrieved.

    Returns
    -------
    list[CourseGet]
        A list of courses taught by the specified teacher
    """
    con = get_connection()
    courses = get_courses_by_teacher(con, teacher_id)
    return courses

@app.put("/courses/{course_id}", response_model=CourseGet)
def update_course_put_route(course_id: int, course: CoursePut):
    """
    Update an existing course by ID.

    This endpoint replaces all fields of an existing course with the data
    provided in the `CoursePut` model. The `course_id` in the path must match
    the `course_id` in the request body; otherwise, a 400 error is raised.
    If the update succeeds, the updated course is returned. Any validation or
    database error results in a 400 HTTPException.

    Parameters
    ----------
    course_id : int
        The ID of the course to update.
    course : CoursePut
        The full course data including title, description, teacher ID,
        start date, and end date.

    Returns
    -------
    CourseGet
        The updated course.

    Raises
    ------
    HTTPException (400)
        If the path ID and body ID do not match, or if the update fails.
    """
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
    """
    Partially update an existing course by ID.

    This endpoint allows updating one or more fields of a course without
    requiring the full course object. Only the fields provided in the
    `CoursePatch` model are modified; any omitted fields retain their
    existing values. If the course does not exist, a 404 error is raised.
    Any validation or database error results in a 400 HTTPException.

    Parameters
    ----------
    course_id : int
        The ID of the course to update.
    course : CoursePatch
        A partial course update model where each field is optional.

    Returns
    -------
    CourseGet
        The updated course after applying the partial changes.

    Raises
    ------
    HTTPException (404)
        If the course does not exist.
    HTTPException (400)
        If the update operation fails.
    """
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
    """
    Delete a course by ID.

    This endpoint removes a course from the system using the provided
    `course_id`. If the deletion is successful, the deleted course is returned
    using the `CourseGet` response model. If the course does not exist or the
    deletion fails, a 404 HTTPException is raised.

    Parameters
    ----------
    course_id : int
        The ID of the course to delete.

    Returns
    -------
    CourseGet
        The data of the deleted course.

    Raises
    ------
    HTTPException (404)
        If the course does not exist or the deletion operation fails.
    """
    con = get_connection()
    try:
        deleted = delete_course(con, course_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# ENROLLMENTS / routes
# -------------------------
@app.post("/enrollments", status_code=201, response_model=EnrollmentGet)
def enroll_user_route(enrollment: EnrollmentCreate):
    """
    Enroll a user in a course.

    This endpoint creates a new enrollment record linking a user to a course,
    using the data provided in the `EnrollmentCreate` model. If the enrollment
    is successful, the newly created enrollment is returned using the
    `EnrollmentGet` response model. Any validation or database error results
    in a 400 HTTPException.

    Parameters
    ----------
    enrollment : EnrollmentCreate
        The enrollment data including user ID and course ID.

    Returns
    -------
    EnrollmentGet
        The newly created enrollment record.

    Raises
    ------
    HTTPException (400)
        If the enrollment cannot be created due to invalid data or a database error.
    """
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
    """
    Get an enrollment by ID.

    This endpoint fetches a single enrollment record using the provided
    `enrollment_id`. If the enrollment does not exist, a 404 HTTPException
    is raised. On success, the enrollment is returned using the
    `EnrollmentGet` response model.

    Parameters
    ----------
    enrollment_id : int
        The ID of the enrollment to retrieve.

    Returns
    -------
    EnrollmentGet
        The requested enrollment record.

    Raises
    ------
    HTTPException (404)
        If the enrollment does not exist.
    """
    con = get_connection()
    enrollment = get_enrollment(con, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@app.get("/users/{user_id}/enrollments", response_model=list[EnrollmentGet])
def get_enrollments_by_user_route(user_id: int):
    """
    Get all enrollments for a specific user.

    This endpoint returns a list of enrollment records associated with the
    given `user_id`. If the user has no enrollments, an empty list is returned.

    Parameters
    ----------
    user_id : int
        The ID of the user whose enrollments should be retrieved.

    Returns
    -------
    list[EnrollmentGet]
        A list of enrollment records for the specified user.
    """
    con = get_connection()
    enrollments = get_enrollments_by_user(con, user_id)
    return enrollments

# -------------------------
# ASSIGNMENTS / routes
# -------------------------
@app.post("/assignments", status_code=201, response_model=AssignmentGet)
def create_assignment_route(assignment: AssignmentCreate):
    """
     Create a new assignment.

    This endpoint creates a new assignment for a course using the data provided
    in the `AssignmentCreate` model. If the creation succeeds, the newly created
    assignment is returned using the `AssignmentGet` response model. Any
    validation or database error results in a 400 HTTPException.

    Parameters
    ----------
    assignment : AssignmentCreate
        The assignment data including course ID, title, description, and due date.

    Returns
    -------
    AssignmentGet
        The newly created assignment.

    Raises
    ------
    HTTPException (400)
        If the assignment cannot be created due to invalid data or a database error.
    """
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
    """
    Get an assignment by ID.

    This endpoint fetches a single assignment using the provided
    `assignment_id`. If the assignment does not exist, a 404 HTTPException
    is raised. On success, the assignment is returned using the
    `AssignmentGet` response model.

    Parameters
    ----------
    assignment_id : int
        The ID of the assignment to retrieve.

    Returns
    -------
    AssignmentGet
        The requested assignment.

    Raises
    ------
    HTTPException (404)
        If the assignment does not exist.
    """
    con = get_connection()
    assignment = get_assignment(con, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@app.get("/courses/{course_id}/assignments", response_model=list[AssignmentGet])
def get_assignments_by_course_route(course_id: int):
    """
    Get all assignments for a specific course.

    This endpoint returns a list of assignments associated with the given
    `course_id`. If the course has no assignments, an empty list is returned.

    Parameters
    ----------
    course_id : int
        The ID of the course whose assignments should be retrieved.

    Returns
    -------
    list[AssignmentGet]
        A list of assignments belonging to the specified course.
    """
    con = get_connection()
    assignments = get_assignments_by_course(con, course_id)
    return assignments

@app.put("/assignments/{assignment_id}", response_model=AssignmentGet)
def update_assignment_put_route(assignment_id: int, assignment: AssignmentGet):
    """
    Update an existing assignment by ID.

    This endpoint replaces all fields of an existing assignment with the data
    provided in the `AssignmentGet` model. The `assignment_id` in the path must
    match the `assignment_id` in the request body; otherwise, a 400 error is
    raised. If the update succeeds, the updated assignment is returned. Any
    validation or database error results in a 400 HTTPException.

    Parameters
    ----------
    assignment_id : int
        The ID of the assignment to update.
    assignment : AssignmentGet
        The full assignment data including course ID, title, description,
        and due date.

    Returns
    -------
    AssignmentGet
        The updated assignment.

    Raises
    ------
    HTTPException (400)
        If the path ID and body ID do not match, or if the update fails.
    """
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
    """
    Partially update an existing assignment by ID.

    This endpoint allows updating one or more fields of an assignment without
    requiring the full assignment object. Only the fields provided in the
    `AssignmentUpdate` model are modified; any omitted fields remain unchanged.
    If the assignment does not exist, a 404 error is raised. If no fields are
    provided for update, a 400 error is returned. Any validation or database
    error results in a 400 HTTPException.

    Parameters
    ----------
    assignment_id : int
        The ID of the assignment to update.
    assignment : AssignmentUpdate
        A partial assignment update model where each field is optional.

    Returns
    -------
    AssignmentGet
        The updated assignment after applying the partial changes.

    Raises
    ------
    HTTPException (404)
        If the assignment does not exist.
    HTTPException (400)
        If no fields are provided or if the update operation fails.
    """
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
    """
    Delete an assignment by ID.

    This endpoint removes an assignment from the system using the provided
    `assignment_id`. If the deletion is successful, the deleted assignment is
    returned using the `AssignmentGet` response model. If the assignment does
    not exist or the deletion fails, a 404 HTTPException is raised.

    Parameters
    ----------
    assignment_id : int
        The ID of the assignment to delete.

    Returns
    -------
    AssignmentGet
        The data of the deleted assignment.

    Raises
    ------
    HTTPException (404)
        If the assignment does not exist or the deletion operation fails.
    """
    con = get_connection()
    try:
        deleted = delete_assignment(con, assignment_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -----------------------------
# MESSAGES / routes
# -----------------------------
@app.post("/messages", status_code=201, response_model=MessageGet)
def send_message_route(message: MessageCreate):
    """
    Send a message between users.

    This endpoint creates a new message using the data provided in the
    `MessageCreate` model. A message may optionally be associated with a
    course. If the creation succeeds, the newly created message is returned
    using the `MessageGet` response model. Any validation or database error
    results in a 400 HTTPException.

    Parameters
    ----------
    message : MessageCreate
        The message data including sender ID, receiver ID, optional course ID,
        and message content.

    Returns
    -------
    MessageGet
        The newly created message.

    Raises
    ------
    HTTPException (400)
        If the message cannot be created due to invalid data or a database error.
    """
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
    """
    Get all messages exchanged between two users.

    This endpoint returns a list of messages exchanged between the two
    specified users. If no messages exist between them, a 404 HTTPException
    is raised.

    Parameters
    ----------
    user1_id : int
        The ID of the first user in the conversation.
    user2_id : int
        The ID of the second user in the conversation.

    Returns
    -------
    list[MessageGet]
        A list of messages exchanged between the two users.

    Raises
    ------
    HTTPException (404)
        If no messages exist between the specified users.
    """
    con = get_connection()

    # Get messages
    messages = get_messages_between_users(con, user1_id, user2_id)

    # If no messages exist, raise 404
    if not messages: 
        raise HTTPException(status_code=404, detail="No messages found between these users")
    
    return messages

# -----------------------------
# SUBMISSION / routes
# -----------------------------
@app.post("/submissions", status_code=201, response_model=SubmissionGet)
def submit_assignment_route(submission: SubmissionCreate):
    """
    Create an assignment.

    This endpoint creates a new submission for a specific assignment using the
    data provided in the `SubmissionCreate` model. If the submission is
    successfully created, the newly created submission is returned using the
    `SubmissionGet` response model. Any validation or database error results
    in a 400 HTTPException.

    Parameters
    ----------
    submission : SubmissionCreate
        The submission data including assignment ID, student ID, and the URL
        to the submitted work.

    Returns
    -------
    SubmissionGet
        The newly created submission record.

    Raises
    ------
    HTTPException (400)
        If the submission cannot be created due to invalid data or a database error.
    """
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
    """
    Get a submission by ID.

    This endpoint fetches a single submission using the provided
    `submission_id`. If the submission does not exist, a 404 HTTPException
    is raised. On success, the submission is returned using the
    `SubmissionGet` response model.

    Parameters
    ----------
    submission_id : int
        The ID of the submission to retrieve.

    Returns
    -------
    SubmissionGet
        The requested submission record.

    Raises
    ------
    HTTPException (404)
        If the submission does not exist.
    """
    con = get_connection()
    submission = get_submission(con, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission

@app.get("/assignments/{assignment_id}/submissions", response_model=list[SubmissionGet])
def get_submissions_by_assignment_route(assignment_id: int):
    """
    Get all submissions for a specific assignment.

    This endpoint returns a list of submissions associated with the given
    `assignment_id`. If the assignment has no submissions, an empty list is
    returned.

    Parameters
    ----------
    assignment_id : int
        The ID of the assignment whose submissions should be retrieved.

    Returns
    -------
    list[SubmissionGet]
        A list of submissions for the specified assignment.
    """
    con = get_connection()
    submissions = get_submissions_by_assignment(con, assignment_id)
    return submissions

@app.get("/students/{student_id}/submissions", response_model=list[SubmissionGet])
def get_submissions_by_student_route(student_id: int):
    """
    Get all submissions made by a specific student.

    This endpoint returns a list of submissions associated with the given
    `student_id`. If the student has not submitted any assignments, an empty
    list is returned.

    Parameters
    ----------
    student_id : int
        The ID of the student whose submissions should be retrieved.

    Returns
    -------
    list[SubmissionGet]
        A list of submissions made by the specified student.
    """
    con = get_connection()
    submissions = get_submissions_by_student(con, student_id)
    return submissions

@app.put("/submissions/{submission_id}/grade", response_model=SubmissionGet)
def grade_submission_route(submission_id: int, grade_data: GradeUpdate):
    """
    Grade a submission.

    This endpoint updates the grade and optional feedback for a specific
    submission using the data provided in the `GradeUpdate` model. If the
    submission does not exist or the update fails, a 404 HTTPException is
    raised. On success, the updated submission is returned using the
    `SubmissionGet` response model.

    Parameters
    ----------
    submission_id : int
        The ID of the submission to grade.
    grade_data : GradeUpdate
        The grading information, including the grade value and optional
        feedback.

    Returns
    -------
    SubmissionGet
        The updated submission with the applied grade and feedback.

    Raises
    ------
    HTTPException (404)
        If the submission does not exist or the grade update fails.
    """
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
    """
    Delete a submission by ID.

    This endpoint removes a submission from the system using the provided
    `submission_id`. If the deletion is successful, the deleted submission is
    returned using the `SubmissionGet` response model. If the submission does
    not exist or the deletion fails, a 404 HTTPException is raised.

    Parameters
    ----------
    submission_id : int
        The ID of the submission to delete.

    Returns
    -------
    SubmissionGet
        The data of the deleted submission.

    Raises
    ------
    HTTPException (404)
        If the submission does not exist or the deletion operation fails.
    """
    con = get_connection()
    try:
        deleted = delete_submission(con, submission_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# LESSONS / routes
# -------------------------
@app.post("/lessons", status_code=201, response_model=LessonGet)
def create_lesson_route(lesson: LessonCreate):
    """
    Create a new lesson.

    This endpoint creates a new lesson for a course using the data provided
    in the `LessonCreate` schema. If the lesson is successfully created, the
    newly created lesson is returned using the `LessonGet` response model.
    Any validation or database error results in a 400 HTTPException.

    Parameters
    ----------
    lesson : LessonCreate
        The lesson data including course ID, title, description, scheduled
        date and time, duration in minutes, and location.

    Returns
    -------
    LessonGet
        The newly created lesson.

    Raises
    ------
    HTTPException (400)
        If the lesson cannot be created due to invalid data or a database error.
    """
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
    """
    Get a lesson by ID.

    This endpoint fetches a single lesson using the provided `lesson_id`. If
    the lesson does not exist, a 404 HTTPException is raised. On success, the
    lesson is returned using the `LessonGet` response model.

    Parameters
    ----------
    lesson_id : int
        The ID of the lesson to retrieve.

    Returns
    -------
    LessonGet
        The requested lesson.

    Raises
    ------
    HTTPException (404)
        If the lesson does not exist.
    """
    con = get_connection()
    lesson = get_lesson(con, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@app.get("/courses/{course_id}/lessons", response_model=list[LessonGet])
def get_lessons_by_course_route(course_id: int):
    """
    Get all lessons for a specific course.

    This endpoint returns a list of lessons associated with the given
    `course_id`. If the course has no lessons, an empty list is returned.

    Parameters
    ----------
    course_id : int
        The ID of the course whose lessons should be retrieved.

    Returns
    -------
    list[LessonGet]
        A list of lessons for the specified course.
    """
    con = get_connection()
    lessons = get_lessons_by_course(con, course_id)
    return lessons

@app.put("/lessons/{lesson_id}", response_model=LessonGet)
def update_lesson_put_route(lesson_id: int, lesson: LessonPut):
    """
    Update an existing lesson by ID.

    This endpoint replaces all fields of an existing lesson with the data
    provided in the `LessonPut` model. The `lesson_id` in the path must match
    the `id` field in the request body; otherwise, a 400 error is raised. If
    the update succeeds, the updated lesson is returned. Any validation or
    database error results in a 400 HTTPException.

    Parameters
    ----------
    lesson_id : int
        The ID of the lesson to update.
    lesson : LessonPut
        The full lesson data including course ID, title, description,
        scheduled date and time, duration in minutes, and location.

    Returns
    -------
    LessonGet
        The updated lesson.

    Raises
    ------
    HTTPException (400)
        If the path ID and body ID do not match, or if the update fails.
    """
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
    """
    Delete a lesson by ID.

    This endpoint removes a lesson from the system using the provided
    `lesson_id`. If the deletion is successful, the deleted lesson is returned
    using the `LessonGet` response model. If the lesson does not exist or the
    deletion fails, a 404 HTTPException is raised.

    Parameters
    ----------
    lesson_id : int
        The ID of the lesson to delete.

    Returns
    -------
    LessonGet
        The data of the deleted lesson.

    Raises
    ------
    HTTPException (404)
        If the lesson does not exist or the deletion operation fails.
    """
    con = get_connection()
    try:
        deleted = delete_lesson(con, lesson_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# RESOURCES / routes
# -------------------------
@app.post("/resources", status_code=201, response_model=ResourceGet)
def create_resource_route(resource: ResourceCreate):
    """
    Create a new resource.

    This endpoint creates a new resource associated with a course or lesson
    using the data provided in the `ResourceCreate` model. If the resource is
    successfully created, the newly created resource is returned using the
    `ResourceGet` response model. Any validation or database error results in
    a 400 HTTPException.

    Parameters
    ----------
    resource : ResourceCreate
        The resource data including course ID, lesson ID, title, type, and URL.

    Returns
    -------
    ResourceGet
        The newly created resource.

    Raises
    ------
    HTTPException (400)
        If the resource cannot be created due to invalid data or a database error.
    """
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
    """
    Get a resource by ID.

    This endpoint fetches a single resource using the provided `resource_id`.
    If the resource does not exist, a 404 HTTPException is raised. On success,
    the resource is returned using the `ResourceGet` response model.

    Parameters
    ----------
    resource_id : int
        The ID of the resource to retrieve.

    Returns
    -------
    ResourceGet
        The requested resource.

    Raises
    ------
    HTTPException (404)
        If the resource does not exist.
    """
    con = get_connection()
    resource = get_resource(con, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@app.get("/courses/{course_id}/resources", response_model=list[ResourceGet])
def get_resources_by_course_route(course_id: int):
    """
    Get all resources for a specific course.

    This endpoint returns a list of resources associated with the given
    `course_id`. If the course has no resources, an empty list is returned.

    Parameters
    ----------
    course_id : int
        The ID of the course whose resources should be retrieved.

    Returns
    -------
    list[ResourceGet]
        A list of resources for the specified course.
    """
    con = get_connection()
    resources = get_resources_by_course(con, course_id)
    return resources

@app.get("/lessons/{lesson_id}/resources", response_model=list[ResourceGet])
def get_resources_by_lesson_route(lesson_id: int):
    """
    Get all resources for a specific lesson.

    This endpoint returns a list of resources associated with the given
    `lesson_id`. If the lesson has no resources, an empty list is returned.

    Parameters
    ----------
    lesson_id : int
        The ID of the lesson whose resources should be retrieved.

    Returns
    -------
    list[ResourceGet]
        A list of resources for the specified lesson.
    """
    con = get_connection()
    resources = get_resources_by_lesson(con, lesson_id)
    return resources

@app.put("/resources/{resource_id}", response_model=ResourceGet)
def update_resource_put_route(resource_id: int, resource: ResourcePut):
    """
    Update an existing resource by ID.

    This endpoint replaces all fields of an existing resource with the data
    provided in the `ResourcePut` model. The `resource_id` in the path must
    match the `resource_id` field in the request body; otherwise, a 400 error
    is raised. If the update succeeds, the updated resource is returned using
    the `ResourceGet` response model. Any validation or database error results
    in a 400 HTTPException.

    Parameters
    ----------
    resource_id : int
        The ID of the resource to update.
    resource : ResourcePut
        The full resource data including course ID, lesson ID, title, type,
        URL, and upload timestamp.

    Returns
    -------
    ResourceGet
        The updated resource.

    Raises
    ------
    HTTPException (400)
        If the path ID and body ID do not match, or if the update fails.
    """
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
    """
    Delete a resource by ID.

    This endpoint removes a resource from the system using the provided
    `resource_id`. If the deletion is successful, the deleted resource is
    returned using the `ResourceGet` response model. If the resource does not
    exist or the deletion fails, a 404 HTTPException is raised.

    Parameters
    ----------
    resource_id : int
        The ID of the resource to delete.

    Returns
    -------
    ResourceGet
        The data of the deleted resource.

    Raises
    ------
    HTTPException (404)
        If the resource does not exist or the deletion operation fails.
    """
    con = get_connection()
    try:
        deleted = delete_resource(con, resource_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------
# ATTENDANCE / routes
# -------------------------
@app.post("/attendance", status_code=201, response_model=AttendanceGet)
def record_attendance_route(attendance: AttendanceCreate):
    """
    Create attendance for a lesson.

    This endpoint creates a new attendance using the data provided in
    the `AttendanceCreate` model. If the record is successfully created, the
    newly created attendance entry is returned using the `AttendanceGet`
    response model. Any validation or database error results in a
    400 HTTPException.

    Parameters
    ----------
    attendance : AttendanceCreate
        The attendance data including lesson ID, student ID, status, and
        optional URL.

    Returns
    -------
    AttendanceGet
        The newly created attendance record.

    Raises
    ------
    HTTPException (400)
        If the attendance record cannot be created due to invalid data or a
        database error.
    """
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
    """
    Get an attendance by ID.

    This endpoint fetches a single attendance record using the provided
    `attendance_id`. If the record does not exist, a 404 HTTPException is
    raised. On success, the attendance entry is returned using the
    `AttendanceGet` response model.

    Parameters
    ----------
    attendance_id : int
        The ID of the attendance record to retrieve.

    Returns
    -------
    AttendanceGet
        The requested attendance record.

    Raises
    ------
    HTTPException (404)
        If the attendance record does not exist.
    """
    con = get_connection()
    attendance = get_attendance(con, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance

@app.get("/lessons/{lesson_id}/attendance", response_model=list[AttendanceGet])
def get_attendance_by_lesson_route(lesson_id: int):
    """
    Get all attendance for a specific lesson.

    This endpoint returns a list of attendance entries associated with the
    given `lesson_id`. If the lesson has no attendance records, an empty list
    is returned.

    Parameters
    ----------
    lesson_id : int
        The ID of the lesson whose attendance records should be retrieved.

    Returns
    -------
    list[AttendanceGet]
        A list of attendance records for the specified lesson.
    """
    con = get_connection()
    attendance = get_attendance_by_lesson(con, lesson_id)
    return attendance

@app.get("/students/{student_id}/attendance", response_model=list[AttendanceGet])
def get_attendance_by_student_route(student_id: int):
    """
    GEt all attendance for a specific student.

    This endpoint returns a list of attendance entries associated with the
    given `student_id`. If the student has no attendance records, an empty
    list is returned.

    Parameters
    ----------
    student_id : int
        The ID of the student whose attendance records should be retrieved.

    Returns
    -------
    list[AttendanceGet]
        A list of attendance records for the specified student.
    """
    con = get_connection()
    attendance = get_attendance_by_student(con, student_id)
    return attendance

@app.put("/attendance/{attendance_id}", response_model=AttendanceGet)
def update_attendance_put_route(attendance_id: int, attendance: AttendancePut):
    """
    Update an existing attendance by ID.

    This endpoint replaces all fields of an existing attendance record with
    the data provided in the `AttendancePut` model. The `attendance_id` in the
    path must match the `attendance_id` field in the request body; otherwise,
    a 400 error is raised. If the update succeeds, the updated attendance
    record is returned using the `AttendanceGet` response model. Any
    validation or database error results in a 400 HTTPException.

    Parameters
    ----------
    attendance_id : int
        The ID of the attendance record to update.
    attendance : AttendancePut
        The full attendance data including lesson ID, student ID, status,
        URL, recorded timestamp, and upload timestamp.

    Returns
    -------
    AttendanceGet
        The updated attendance record.

    Raises
    ------
    HTTPException (400)
        If the path ID and body ID do not match, or if the update fails.
    """
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
    """
    Delete an attendance by ID.

    This endpoint removes an attendance record from the system using the
    provided `attendance_id`. If the deletion is successful, the deleted
    attendance entry is returned using the `AttendanceGet` response model.
    If the record does not exist or the deletion fails, a 404 HTTPException
    is raised.

    Parameters
    ----------
    attendance_id : int
        The ID of the attendance record to delete.

    Returns
    -------
    AttendanceGet
        The data of the deleted attendance record.

    Raises
    ------
    HTTPException (404)
        If the attendance record does not exist or the deletion operation fails.
    """
    con = get_connection()
    try:
        deleted = delete_attendance(con, attendance_id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
