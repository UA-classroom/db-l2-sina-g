import psycopg2
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""

### THIS IS JUST AN EXAMPLE OF A FUNCTION FOR INSPIRATION FOR A LIST-OPERATION (FETCHING MANY ENTRIES)
# def get_items(con):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("SELECT * FROM items;")
#             items = cursor.fetchall()
#     return items


### THIS IS JUST INSPIRATION FOR A DETAIL OPERATION (FETCHING ONE ENTRY)
# def get_item(con, item_id):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("""SELECT * FROM items WHERE id = %s""", (item_id,))
#             item = cursor.fetchone()
#             return item


### THIS IS JUST INSPIRATION FOR A CREATE-OPERATION
# def add_item(con, title, description):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "INSERT INTO items (title, description) VALUES (%s, %s) RETURNING id;",
#                 (title, description),
#             )
#             item_id = cursor.fetchone()["id"]
#     return item_id

# -------------------------
# USERS
# -------------------------

def create_user(con, username, email, role, password):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, email, role, password)
                VALUES (%s, %s, %s, %s)
                RETURNING user_id;
                """,
                (username, email, role, password),
            )
            user = cursor.fetchone()
    return user


def get_user(con, user_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            user = cursor.fetchone()
    return user


def get_all_users(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
    return users


# -------------------------
# COURSES
# -------------------------

def create_course(con, title, description, teacher_id, start_date, end_date):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO courses (title, description, teacher_id, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING course_id;
                """,
                (title, description, teacher_id, start_date, end_date),
            )
            course = cursor.fetchone()
    return course


def get_course(con, course_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM courses WHERE course_id = %s;", (course_id,))
            course = cursor.fetchone()
    return course


def get_courses_by_teacher(con, teacher_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM courses WHERE teacher_id = %s;",
                (teacher_id,),
            )
            courses = cursor.fetchall()
    return courses

# -------------------------
# LESSONS
# -------------------------

def create_lesson(con, course_id, title, description, scheduled_at, duration_minutes, location):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO lessons (course_id, title, description, scheduled_at, duration_minutes, location)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING lesson_id;
                """,
                (course_id, title, description, scheduled_at, duration_minutes, location),
            )
            lesson = cursor.fetchone()
    return lesson


def get_lessons_for_course(con, course_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM lessons WHERE course_id = %s ORDER BY scheduled_at;",
                (course_id,),
            )
            lessons = cursor.fetchall()
    return lessons

# -------------------------
# ENROLLMENTS
# -------------------------

def enroll_user(con, user_id, course_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO enrollments (user_id, course_id)
                    VALUES (%s, %s)
                    RETURNING enrollment_id;
                    """,
                    (user_id, course_id),
                )
                enrollment = cursor.fetchone()
            except psycopg2.Error:
                raise Exception("User is already enrolled or invalid IDs.")
    return enrollment


def get_enrolled_students(con, course_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT u.user_id, u.username, u.email
                FROM enrollments e
                JOIN users u ON u.user_id = e.user_id
                WHERE e.course_id = %s;
                """,
                (course_id,),
            )
            students = cursor.fetchall()
    return students

# -------------------------
# ASSIGNMENTS
# -------------------------

def create_assignment(con, course_id, title, description, due_date):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO assignments (course_id, title, description, due_date)
                VALUES (%s, %s, %s, %s)
                RETURNING assignment_id;
                """,
                (course_id, title, description, due_date),
            )
            assignment = cursor.fetchone()
    return assignment

def get_assignments_for_course(con, course_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM assignments WHERE course_id = %s ORDER BY due_date;",
                (course_id,),
            )
            assignments = cursor.fetchall()
    return assignments

# -------------------------
# SUBMISSIONS
# -------------------------

def submit_assignment(con, assignment_id, student_id, url):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO submissions (assignment_id, student_id, url)
                VALUES (%s, %s, %s)
                RETURNING submission_id;
                """,
                (assignment_id, student_id, url),
            )
            submission = cursor.fetchone()
    return submission

def grade_submission(con, submission_id, grade, feedback):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE submissions
                SET grade = %s, feedback = %s
                WHERE submission_id = %s
                RETURNING submission_id;
                """,
                (grade, feedback, submission_id),
            )
            updated = cursor.fetchone()
            if not updated:
                raise Exception("Submission not found.")
    return updated

# -------------------------
# MESSAGES
# -------------------------

def send_message(con, sender_id, receiver_id, course_id, content):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO messages (sender_id, receiver_id, course_id, content)
                VALUES (%s, %s, %s, %s)
                RETURNING message_id;
                """,
                (sender_id, receiver_id, course_id, content),
            )
            message = cursor.fetchone()
    return message

def get_messages_between_users(con, user1, user2):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM messages
                WHERE (sender_id = %s AND receiver_id = %s)
                   OR (sender_id = %s AND receiver_id = %s)
                ORDER BY sent_at;
                """,
                (user1, user2, user2, user1),
            )
            messages = cursor.fetchall()
    return messages

# -------------------------
# RESOURCES
# -------------------------

def add_resource(con, course_id, lesson_id, title, type, url):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO resources (course_id, lesson_id, title, type, url)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING resource_id;
                """,
                (course_id, lesson_id, title, type, url),
            )
            resource = cursor.fetchone()
    return resource

def get_resources_for_course(con, course_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM resources WHERE course_id = %s;",
                (course_id,),
            )
            resources = cursor.fetchall()
    return resources

# -------------------------
# ATTENDANCE
# -------------------------

def record_attendance(con, lesson_id, student_id, status, url=None):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO attendance (lesson_id, student_id, status, url)
                VALUES (%s, %s, %s, %s)
                RETURNING attendance_id;
                """,
                (lesson_id, student_id, status, url),
            )
            attendance = cursor.fetchone()
    return attendance


def get_attendance_for_lesson(con, lesson_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT a.*, u.username
                FROM attendance a
                JOIN users u ON u.user_id = a.student_id
                WHERE lesson_id = %s;
                """,
                (lesson_id,),
            )
            attendance = cursor.fetchall()
    return attendance