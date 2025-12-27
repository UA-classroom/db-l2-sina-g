import psycopg2
from psycopg2.extras import RealDictCursor

# -----------------------------------------------------
# USERS
# -----------------------------------------------------
def create_user(con, username, email, role, password):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO users (username, email, role, password)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                """, (username, email, role, password))
                return cursor.fetchone()
    except psycopg2.IntegrityError:
        raise Exception("User creation failed: email already exists or invalid role.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_user_by_id(con, user_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
                return cursor.fetchone()
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_all_users(con):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM users;")
                return cursor.fetchall()
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def update_user(con, user_id, username, email, role):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE users
                    SET username = %s,
                        email = %s,
                        role = %s
                    WHERE user_id = %s
                    RETURNING *;
                """, (username, email, role, user_id))
                user = cursor.fetchone()
                if not user:
                    raise Exception("User not found.")
                return user
    except psycopg2.IntegrityError:
        raise Exception("User update failed: email already exists or invalid role.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def delete_user(con, user_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("DELETE FROM users WHERE user_id = %s RETURNING *;", (user_id,))
                user = cursor.fetchone()
                if not user:
                    raise Exception("User not found.")
                return user
    except psycopg2.Error as e:
        raise Exception(f"User delete failed: {e.pgerror}") from e

# -----------------------------------------------------
# COURSES
# -----------------------------------------------------
def create_course(con, title, description, teacher_id, start_date, end_date):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO courses (title, description, teacher_id, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *;
                """, (title, description, teacher_id, start_date, end_date))
                return cursor.fetchone()

    except psycopg2.IntegrityError:
        raise Exception("Course creation failed: invalid teacher_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_course(con, course_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM courses WHERE course_id = %s;",
                    (course_id,)
                )
                return cursor.fetchone()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_courses_by_teacher(con, teacher_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM courses WHERE teacher_id = %s;",
                    (teacher_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def update_course(con, course_id, title, description, teacher_id, start_date, end_date):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE courses
                    SET title = %s,
                        description = %s,
                        teacher_id = %s,
                        start_date = %s,
                        end_date = %s
                    WHERE course_id = %s
                    RETURNING *;
                """, (title, description, teacher_id, start_date, end_date, course_id))

                course = cursor.fetchone()
                if not course:
                    raise Exception("Course not found.")
                return course

    except psycopg2.Error as e:
        raise Exception(f"Course update failed: {e.pgerror}") from e

def delete_course(con, course_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM courses WHERE course_id = %s RETURNING *;",
                    (course_id,)
                )
                course = cursor.fetchone()
                if not course:
                    raise Exception("Course not found.")
                return course

    except psycopg2.Error as e:
        raise Exception(f"Course delete failed: {e.pgerror}") from e
    
#---------------------------------------------
# Enrollment
# --------------------------------------------
def create_enrollment(con, user_id, course_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO enrollments (user_id, course_id)
                    VALUES (%s, %s)
                    RETURNING *;
                """, (user_id, course_id))
                return cursor.fetchone()

    except psycopg2.IntegrityError:
        raise Exception("Enrollment failed: invalid user_id or course_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_enrollment(con, enrollment_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM enrollments WHERE enrollment_id = %s;",
                    (enrollment_id,)
                )
                return cursor.fetchone()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_enrollments_by_user(con, user_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM enrollments WHERE user_id = %s;",
                    (user_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
# -------------------------------------------
# Assigment
# -------------------------------------------
def create_assignment(con, course_id, title, description, due_date):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO assignments (course_id, title, description, due_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                """, (course_id, title, description, due_date))
                return cursor.fetchone()

    except psycopg2.IntegrityError:
        raise Exception("Assignment creation failed: invalid course_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
def get_assignment(con, assignment_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM assignments WHERE assignment_id = %s;",
                    (assignment_id,)
                )
                return cursor.fetchone()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_assignments_by_course(con, course_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM assignments WHERE course_id = %s;",
                    (course_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def update_assignment(con, assignment_id, course_id, title, description, due_date):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE assignments
                    SET course_id = %s,
                        title = %s,
                        description = %s,
                        due_date = %s
                    WHERE assignment_id = %s
                    RETURNING *;
                """, (course_id, title, description, due_date, assignment_id))

                assignment = cursor.fetchone()
                if not assignment:
                    raise Exception("Assignment not found.")
                return assignment

    except psycopg2.Error as e:
        raise Exception(f"Assignment update failed: {e.pgerror}") from e

def delete_assignment(con, assignment_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM assignments WHERE assignment_id = %s RETURNING *;",
                    (assignment_id,)
                )
                assignment = cursor.fetchone()
                if not assignment:
                    raise Exception("Assignment not found.")
                return assignment

    except psycopg2.Error as e:
        raise Exception(f"Assignment delete failed: {e.pgerror}") from e
    
# -------------------------------------------
# MESSAGES
# -------------------------------------------
def create_message(con, sender_id, receiver_id, course_id, content):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO messages (sender_id, receiver_id, course_id, content)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                """, (sender_id, receiver_id, course_id, content))
                return cursor.fetchone()

    except psycopg2.IntegrityError:
        raise Exception("Message creation failed: invalid sender_id, receiver_id, or course_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
def get_messages_between_users(con, user1_id, user2_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM messages
                    WHERE (sender_id = %s AND receiver_id = %s)
                       OR (sender_id = %s AND receiver_id = %s)
                    ORDER BY sent_at ASC;
                """, (user1_id, user2_id, user2_id, user1_id))
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
# -------------------------------------------
# SUBMISSION
# -------------------------------------------
def create_submission(con, assignment_id, student_id, url):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO submissions (assignment_id, student_id, url)
                    VALUES (%s, %s, %s)
                    RETURNING *;
                """, (assignment_id, student_id, url))
                return cursor.fetchone()

    except psycopg2.IntegrityError:
        raise Exception("Submission failed: invalid assignment_id or student_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_submission(con, submission_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM submissions WHERE submission_id = %s;",
                    (submission_id,)
                )
                return cursor.fetchone()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_submissions_by_assignment(con, assignment_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM submissions WHERE assignment_id = %s;",
                    (assignment_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_submissions_by_student(con, student_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM submissions WHERE student_id = %s;",
                    (student_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

# Grade / Update Submission
def update_submission_grade(con, submission_id, grade, feedback):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE submissions
                    SET grade = %s,
                        feedback = %s
                    WHERE submission_id = %s
                    RETURNING *;
                """, (grade, feedback, submission_id))

                submission = cursor.fetchone()
                if not submission:
                    raise Exception("Submission not found.")
                return submission

    except psycopg2.Error as e:
        raise Exception(f"Submission update failed: {e.pgerror}") from e
    
def delete_submission(con, submission_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM submissions WHERE submission_id = %s RETURNING *;",
                    (submission_id,)
                )
                submission = cursor.fetchone()
                if not submission:
                    raise Exception("Submission not found.")
                return submission

    except psycopg2.Error as e:
        raise Exception(f"Submission delete failed: {e.pgerror}") from e

# -------------------------------------------
# LESSONS
# -------------------------------------------
def create_lesson(con, course_id, title, description, scheduled_at, duration_minutes, location):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO lessons (course_id, title, description, scheduled_at, duration_minutes, location)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *;
                """, (course_id, title, description, scheduled_at, duration_minutes, location))
                return cursor.fetchone()

    except psycopg2.IntegrityError:
        raise Exception("Lesson creation failed: invalid course_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_lesson(con, lesson_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM lessons WHERE lesson_id = %s;",
                    (lesson_id,)
                )
                return cursor.fetchone()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_lessons_by_course(con, course_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM lessons WHERE course_id = %s ORDER BY scheduled_at ASC;",
                    (course_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def update_lesson(con, lesson_id, course_id, title, description, scheduled_at, duration_minutes, location):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE lessons
                    SET course_id = %s,
                        title = %s,
                        description = %s,
                        scheduled_at = %s,
                        duration_minutes = %s,
                        location = %s
                    WHERE lesson_id = %s
                    RETURNING *;
                """, (course_id, title, description, scheduled_at, duration_minutes, location, lesson_id))

                lesson = cursor.fetchone()
                if not lesson:
                    raise Exception("Lesson not found.")
                return lesson

    except psycopg2.Error as e:
        raise Exception(f"Lesson update failed: {e.pgerror}") from e

def delete_lesson(con, lesson_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM lessons WHERE lesson_id = %s RETURNING *;",
                    (lesson_id,)
                )
                lesson = cursor.fetchone()
                if not lesson:
                    raise Exception("Lesson not found.")
                return lesson

    except psycopg2.Error as e:
        raise Exception(f"Lesson delete failed: {e.pgerror}") from e

# -------------------------------------------
# RESOURCES
# -------------------------------------------
def create_resource(con, course_id, lesson_id, title, type, url):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO resources (course_id, lesson_id, title, type, url)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *;
                """, (course_id, lesson_id, title, type, url))
                return cursor.fetchone()

    except psycopg2.IntegrityError:
        raise Exception("Resource creation failed: invalid course_id or lesson_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_resource(con, resource_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM resources WHERE resource_id = %s;",
                    (resource_id,)
                )
                return cursor.fetchone()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_resources_by_course(con, course_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM resources WHERE course_id = %s ORDER BY uploaded_at DESC;",
                    (course_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
def get_resources_by_lesson(con, lesson_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM resources WHERE lesson_id = %s ORDER BY uploaded_at DESC;",
                    (lesson_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
def update_resource(con, resource_id, course_id, lesson_id, title, type, url, uploaded_at):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE resources
                    SET course_id = %s,
                        lesson_id = %s,
                        title = %s,
                        type = %s,
                        url = %s,
                        uploaded_at = %s
                    WHERE resource_id = %s
                    RETURNING *;
                """, (course_id, lesson_id, title, type, url, uploaded_at, resource_id))

                resource = cursor.fetchone()
                if not resource:
                    raise Exception("Resource not found.")
                return resource

    except psycopg2.Error as e:
        raise Exception(f"Resource update failed: {e.pgerror}") from e
    
def delete_resource(con, resource_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM resources WHERE resource_id = %s RETURNING *;",
                    (resource_id,)
                )
                resource = cursor.fetchone()
                if not resource:
                    raise Exception("Resource not found.")
                return resource

    except psycopg2.Error as e:
        raise Exception(f"Resource delete failed: {e.pgerror}") from e

# -------------------------------------------
# ATTENDANCE
# -------------------------------------------
def create_attendance(con, lesson_id, student_id, status, url):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO attendance (lesson_id, student_id, status, url)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                """, (lesson_id, student_id, status, url))
                return cursor.fetchone()

    except psycopg2.IntegrityError:
        raise Exception("Attendance creation failed: invalid lesson_id or student_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
def get_attendance(con, attendance_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM attendance WHERE attendance_id = %s;",
                    (attendance_id,)
                )
                return cursor.fetchone()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
def get_attendance_by_lesson(con, lesson_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM attendance WHERE lesson_id = %s ORDER BY recorded_at ASC;",
                    (lesson_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
def get_attendance_by_student(con, student_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM attendance WHERE student_id = %s ORDER BY recorded_at ASC;",
                    (student_id,)
                )
                return cursor.fetchall()

    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e
    
def update_attendance(con, attendance_id, lesson_id, student_id, status, url, recorded_at, uploaded_at):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE attendance
                    SET lesson_id = %s,
                        student_id = %s,
                        status = %s,
                        url = %s,
                        recorded_at = %s,
                        uploaded_at = %s
                    WHERE attendance_id = %s
                    RETURNING *;
                """, (lesson_id, student_id, status, url, recorded_at, uploaded_at, attendance_id))

                attendance = cursor.fetchone()
                if not attendance:
                    raise Exception("Attendance record not found.")
                return attendance

    except psycopg2.Error as e:
        raise Exception(f"Attendance update failed: {e.pgerror}") from e
    
def delete_attendance(con, attendance_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM attendance WHERE attendance_id = %s RETURNING *;",
                    (attendance_id,)
                )
                attendance = cursor.fetchone()
                if not attendance:
                    raise Exception("Attendance record not found.")
                return attendance

    except psycopg2.Error as e:
        raise Exception(f"Attendance delete failed: {e.pgerror}") from e