# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure

from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr

# --- USER ---
class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(..., pattern="^(teacher|student|admin)$")

class UserGet(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str

class UserPatch(BaseModel):
    username: str | None = Field(None, max_length=50)
    email: EmailStr | None = None
    role: str | None = Field(None, pattern="^(teacher|student|admin)$")

class UserPut(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str

class UserDelete(BaseModel):
    user_id: int

# --- COURSE ---
class CourseGet(BaseModel):
    id: int
    title: str
    description: str | None = None
    teacher_id: int
    start_date: date | None = None
    end_date: date | None = None

class CourseCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    teacher_id: int
    start_date: date | None = None
    end_date: date | None = None

class CoursePatch(BaseModel):
    """For partially updating a course."""
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    teacher_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None

class CoursePut(BaseModel):
    """For fully replacing a course."""
    id: int
    title: str = Field(..., max_length=255)
    description: str | None = None
    teacher_id: int
    start_date: date | None = None
    end_date: date | None = None

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
    description: str | None = None
    due_date: datetime | None = None

class AssignmentCreate(BaseModel):
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None = None
    due_date: datetime | None = None

# --- MESSAGE ---
class MessageGet(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    course_id: int | None = None
    content: str
    sent_at: datetime

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    course_id: int | None = None
    content: str

# --- SUBMISSION ---
class SubmissionGet(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submitted_at: datetime
    url: str | None = None
    grade: str | None = None
    feedback: str | None = None

class SubmissionCreate(BaseModel):
    assignment_id: int
    student_id: int
    url: str | None = None

class GradeUpdate(BaseModel):
    grade: str | None = None
    feedback: str | None = None

# --- LESSON ---
class LessonGet(BaseModel):
    id: int
    course_id: int
    title: str
    description: str | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    location: str | None = None

class LessonCreate(BaseModel):
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    location: str | None = None

class LessonPut(BaseModel):
    id: int
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    location: str | None = None

class LessonDelete(BaseModel):
    id: int

# --- RESOURCE ---
class ResourceGet(BaseModel):
    id: int
    course_id: int
    lesson_id: int | None = None
    title: str
    type: str | None = None
    url: str
    uploaded_at: datetime

class ResourceCreate(BaseModel):
    course_id: int
    lesson_id: int | None = None
    title: str = Field(..., max_length=255)
    type: str | None = None
    url: str

class ResourcePut(BaseModel):
    id: int
    course_id: int
    lesson_id: int | None = None
    title: str = Field(..., max_length=255)
    type: str | None = None
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
    url: str | None = None
    uploaded_at: datetime   

class AttendanceCreate(BaseModel):
    lesson_id: int
    student_id: int
    status: str = Field(..., pattern="^(present|absent|late)$")
    url: str | None = None

class AttendancePut(BaseModel):
    id: int
    lesson_id: int
    student_id: int
    status: str = Field(..., pattern="^(present|absent|late)$")
    url: str | None = None
    recorded_at: datetime
    uploaded_at: datetime

class AttendanceDelete(BaseModel):
    id: int