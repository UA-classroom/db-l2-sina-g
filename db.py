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


# -------------------------------------------
# USERS
# -------------------------------------------

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

# -------------------------------------------
# COURSES
# -------------------------------------------

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
                cursor.execute("SELECT * FROM courses WHERE course_id = %s;", (course_id,))
                return cursor.fetchone()
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_courses_by_teacher(con, teacher_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM courses WHERE teacher_id = %s;", (teacher_id,))
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
                cursor.execute("DELETE FROM courses WHERE course_id = %s RETURNING *;", (course_id,))
                course = cursor.fetchone()
                if not course:
                    raise Exception("Course not found.")
                return course
    except psycopg2.Error as e:
        raise Exception(f"Course delete failed: {e.pgerror}") from e

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

def get_lessons(con, course_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM lessons
                    WHERE course_id = %s
                    ORDER BY scheduled_at;
                """, (course_id,))
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
                cursor.execute("DELETE FROM lessons WHERE lesson_id = %s RETURNING *;", (lesson_id,))
                lesson = cursor.fetchone()
                if not lesson:
                    raise Exception("Lesson not found.")
                return lesson
    except psycopg2.Error as e:
        raise Exception(f"Lesson delete failed: {e.pgerror}") from e

# -------------------------------------------
# RESOURCES
# -------------------------------------------

def add_resource(con, course_id, lesson_id, title, resource_type, url):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO resources (course_id, lesson_id, title, type, url)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *;
                """, (course_id, lesson_id, title, resource_type, url))
                return cursor.fetchone()
    except psycopg2.IntegrityError:
        raise Exception("Resource creation failed: invalid course_id or lesson_id.")
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def get_resources(con, course_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM resources WHERE course_id = %s;", (course_id,))
                return cursor.fetchall()
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def update_resource(con, resource_id, course_id, lesson_id, title, resource_type, url):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE resources
                    SET course_id = %s,
                        lesson_id = %s,
                        title = %s,
                        type = %s,
                        url = %s
                    WHERE resource_id = %s
                    RETURNING *;
                """, (course_id, lesson_id, title, resource_type, url, resource_id))
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
                cursor.execute("DELETE FROM resources WHERE resource_id = %s RETURNING *;", (resource_id,))
                resource = cursor.fetchone()
                if not resource:
                    raise Exception("Resource not found.")
                return resource
    except psycopg2.Error as e:
        raise Exception(f"Resource delete failed: {e.pgerror}") from e

# -------------------------------------------
# ATTENDANCE
# -------------------------------------------

def create_attendance(con, lesson_id, student_id, status, url=None):
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

def get_attendance(con, lesson_id):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT a.*, u.username
                    FROM attendance a
                    JOIN users u ON u.user_id = a.student_id
                    WHERE lesson_id = %s;
                """, (lesson_id,))
                return cursor.fetchall()
    except psycopg2.Error as e:
        raise Exception(f"Database error: {e.pgerror}") from e

def update_attendance(con, attendance_id, lesson_id, student_id, status, url):
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE attendance
                    SET lesson_id = %s,
                        student_id = %s,
                        status = %s,
                        url = %s
                    WHERE attendance_id = %s
                    RETURNING *;
                """, (lesson_id, student_id, status, url, attendance_id))
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
                cursor.execute("DELETE FROM attendance WHERE attendance_id = %s RETURNING *;", (attendance_id,))
                attendance = cursor.fetchone()
                if not attendance:
                    raise Exception("Attendance record not found.")
                return attendance
    except psycopg2.Error as e:
        raise Exception(f"Attendance delete failed: {e.pgerror}") from e