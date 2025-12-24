# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure

# - At least 5-10 GET-endpoints done
# - At least 5-10 POST-endpoints done
# - At least 5-10 PUT-endpoints
# - At least 5 DELETE-endpoints
# - At least 1-2 PATCH endpoints done

from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr

# --- USER ---
class UserGet(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(..., regex="^(teacher|student|admin)$")

class UserPatch(BaseModel):
    """For updating a user."""
    username: str | None = Field(None, max_length=50)
    role: str | None = Field(None, regex="^(teacher|student|admin)$")

class UserPut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

class UserDelete(BaseModel):
    id: int

# --- COURSE ---
class CourseGet(BaseModel):
    id: int
    title: str
    description: str | None
    teacher_id: int
    start_date: date | None
    end_date: date | None

class CourseCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None
    teacher_id: int
    start_date: date | None
    end_date: date | None

class CoursePatch(BaseModel):
    """
    For partially updating a course.
    If a field is None, we skip updating it.
    """
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    teacher_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None

class CoursePut(BaseModel):
    """
    For fully replacing a course.
    All fields must be provided.
    """
    id: int
    title: str = Field(..., max_length=255)
    description: str | None
    teacher_id: int
    start_date: date | None
    end_date: date | None

class CourseDelete(BaseModel):
    id: int

# --- ENROLLMENT ---
class EnrollmentGet(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

# --- ASSIGNMENT ---
class AssignmentGet(BaseModel):
    id: int
    course_id: int
    title: str
    description: str | None
    due_date: datetime | None

class AssignmentCreate(BaseModel):
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None
    due_date: datetime | None

# --- MESSAGE ---
class MessageGet(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    course_id: int | None
    content: str
    sent_at: datetime

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    course_id: int | None
    content: str

# --- SUBMISSION ---
class SubmissionGet(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submitted_at: datetime
    url: str | None
    grade: str | None
    feedback: str | None

class SubmissionCreate(BaseModel):
    assignment_id: int
    student_id: int
    url: str | None

class GradeUpdate(BaseModel):
    grade: str | None
    feedback: str | None

# --- LESSON ---
class LessonGet(BaseModel):
    id: int
    course_id: int
    title: str
    description: str | None
    scheduled_at: datetime | None
    duration_minutes: int | None
    location: str | None

class LessonCreate(BaseModel):
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None
    scheduled_at: datetime | None
    duration_minutes: int | None
    location: str | None

class LessonPut(BaseModel):
    id: int
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None
    scheduled_at: datetime | None
    duration_minutes: int | None
    location: str | None

class LessonDelete(BaseModel):
    id: int

# --- RESOURCE ---
class ResourceGet(BaseModel):
    id: int
    course_id: int
    lesson_id: int | None
    title: str
    type: str | None
    url: str
    uploaded_at: datetime

class ResourceCreate(BaseModel):
    course_id: int
    lesson_id: int | None
    title: str = Field(..., max_length=255)
    type: str | None
    url: str

class ResourcePut(BaseModel):
    id: int
    course_id: int
    lesson_id: int | None
    title: str = Field(..., max_length=255)
    type: str | None
    url: str
    uploaded_at: datetime

class ResourceDelete(BaseModel):
    id: int


# --- ATTENDANCE ---
class AttendanceGet(BaseModel):
    id: int
    lesson_id: int
    student_id: int
    status: str
    recorded_at: datetime
    url: str | None
    uploaded_at: datetime

class AttendanceCreate(BaseModel):
    lesson_id: int
    student_id: int
    status: str = Field(..., regex="^(present|absent|late)$")
    url: str | None

class AttendancePut(BaseModel):
    id: int
    lesson_id: int
    student_id: int
    status: str = Field(..., regex="^(present|absent|late)$")
    url: str | None
    recorded_at: datetime
    uploaded_at: datetime

class AttendanceDelete(BaseModel):
    id: int
