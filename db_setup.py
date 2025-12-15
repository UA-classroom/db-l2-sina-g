import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )

def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    connection = get_connection()
    
    user_table = """
    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(320) UNIQUE NOT NULL,
        role VARCHAR(15) NOT NULL, -- 'teacher' or 'student' or 'admin'
        password TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    courses_table ="""
    CREATE TABLE IF NOT EXISTS courses(
        course_id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        teacher_id INT NOT NULL REFERENCES users(user_id),
        start_date DATE,
        end_date DATE
    );
    """
    enrollments_table ="""
    CREATE TABLE IF NOT EXISTS enrollments(
        enrollment_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users(user_id),
        course_id INT NOT NULL REFERENCES courses(course_id),
        enrolled_at TIMESTAMP DEFAULT NOW(),
        UNIQUE (user_id, course_id)
    );
    """

    assignments_table ="""
    CREATE TABLE IF NOT EXISTS assignments(
        assignment_id SERIAL PRIMARY KEY,
        course_id INT NOT NULL REFERENCES courses(course_id),
        title VARCHAR(255) NOT NULL,
        description TEXT,
        due_date TIMESTAMP   
    );
    """

    messages_table ="""
    CREATE TABLE IF NOT EXISTS messages(
        message_id SERIAL PRIMARY KEY,
        sender_id INT NOT NULL REFERENCES users(user_id),
        receiver_id INT NOT NULL REFERENCES users(user_id),
        course_id INT REFERENCES courses(course_id),
        content TEXT NOT NULL,
        sent_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """

    submissions_table ="""
    CREATE TABLE IF NOT EXISTS submissions(
        submission_id SERIAL PRIMARY KEY,
        assignment_id INT NOT NULL REFERENCES assignments(assignment_id),
        student_id INT NOT NULL REFERENCES users(user_id),
        submitted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        url TEXT,
        grade VARCHAR(20),
        feedback TEXT
    );
    """

    resources_table ="""
    CREATE TABLE IF NOT EXISTS resources(
        resource_id SERIAL PRIMARY KEY,
        course_id INT NOT NULL REFERENCES courses(course_id),
        lesson_id INT REFERENCES lessons(lesson_id),  -- optional
        title VARCHAR(255) NOT NULL,
        type VARCHAR(50),     -- e.g., PDF, video, link
        url TEXT NOT NULL,
        uploaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """

    attendance_table ="""
    CREATE TABLE IF NOT EXISTS attendance(
        attendance_id SERIAL PRIMARY KEY,
        lesson_id INT NOT NULL REFERENCES lessons(lesson_id),
        student_id INT NOT NULL REFERENCES users(user_id),
        status VARCHAR(50) NOT NULL,   -- present/absent/late
        recorded_at TIMESTAMP DEFAULT NOW(),
        url TEXT,                      -- optional attachment
        uploaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """

    lessons_table ="""
    CREATE TABLE IF NOT EXISTS lessons(
        lesson_id SERIAL PRIMARY KEY,
        course_id INT NOT NULL REFERENCES courses(course_id),
        title VARCHAR(255) NOT NULL,
        description TEXT,
        scheduled_at TIMESTAMP,
        duration_minutes INT,
        location VARCHAR(255)
    );
    """

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(user_table)
            cursor.execute(courses_table)
            cursor.execute(lessons_table)
            cursor.execute(enrollments_table)
            cursor.execute(assignments_table)
            cursor.execute(messages_table)
            cursor.execute(submissions_table)
            cursor.execute(resources_table)
            cursor.execute(attendance_table)

    if connection:
        connection.close()

if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
