from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr

# --- USER ---

# Create user 
class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8) # Password need to minimum 8 characters
    role: str = Field(..., pattern="^(teacher|student|admin)$") # When creating new user it can only be teacher|student|admin

# GET user 
class UserGet(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str

# PATCH user
class UserPatch(BaseModel):
    username: str | None = Field(None, max_length=50)
    email: EmailStr | None = None
    role: str | None = Field(None, pattern="^(teacher|student|admin)$")

# PUT user
class UserPut(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str

class UserDelete(BaseModel):
    user_id: int

# --- COURSE ---

# Create Course
class CourseCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    teacher_id: int
    start_date: date | None = None
    end_date: date | None = None

# GET Course
class CourseGet(BaseModel):
    title: str
    description: str | None = None
    teacher_id: int
    start_date: date | None = None
    end_date: date | None = None

# PATCH Course
class CoursePatch(BaseModel):
    """For partially updating a course."""
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    teacher_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None

# PUT Course
class CoursePut(BaseModel):
    """For fully replacing a course."""
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None = None
    teacher_id: int
    start_date: date | None = None
    end_date: date | None = None

# DELETE Course
class CourseDelete(BaseModel):
    id: int

# --- ENROLLMENT ---

# Create Enrollment
class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

# GET Enrollment
class EnrollmentGet(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime

# --- ASSIGNMENT ---

# Create Assigment
class AssignmentCreate(BaseModel):
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None = None
    due_date: datetime | None = None

# GET Assigment
class AssignmentGet(BaseModel):
    assignment_id: int
    course_id: int
    title: str
    description: str | None = None
    due_date: datetime | None = None

# Update Assigment | PATCH
class AssignmentUpdate(BaseModel):
    course_id: int | None = None
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    due_date: datetime | None = None

# --- MESSAGE ---

# Create Message
class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    course_id: int | None = None
    content: str

# GET Messages
class MessageGet(BaseModel):
    message_id: int
    sender_id: int
    receiver_id: int
    course_id: int | None = None
    content: str
    sent_at: datetime

# --- SUBMISSION ---

# Create Submission
class SubmissionCreate(BaseModel):
    assignment_id: int
    student_id: int
    url: str | None = None

# GET Submission
class SubmissionGet(BaseModel):
    submission_id: int
    assignment_id: int
    student_id: int
    submitted_at: datetime
    url: str | None = None
    grade: str | None = None
    feedback: str | None = None

# Updating Grades 
# Grades comes after the submission been finished, thats why it need to be added last
class GradeUpdate(BaseModel):
    grade: str | None = None
    feedback: str | None = None

# --- LESSON ---

# Create Lesson
class LessonCreate(BaseModel):
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    location: str | None = None

# GET Lesson
class LessonGet(BaseModel):
    lesson_id: int
    course_id: int
    title: str
    description: str | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    location: str | None = None

# PUT Lesson
class LessonPut(BaseModel):
    lesson_id: int
    course_id: int
    title: str = Field(..., max_length=255)
    description: str | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None # Time lesson will extend 
    location: str | None = None # Where lesson will be hold

# DELETE Lesson
class LessonDelete(BaseModel):
    id: int

# --- RESOURCE ---

# GET Resource
class ResourceGet(BaseModel):
    resource_id: int
    course_id: int
    lesson_id: int | None = None
    title: str
    type: str | None = None
    url: str
    uploaded_at: datetime

# Create Resource
class ResourceCreate(BaseModel):
    course_id: int
    lesson_id: int | None = None
    title: str = Field(..., max_length=255)
    type: str | None = None
    url: str

# PUT Resource
class ResourcePut(BaseModel):
    resource_id: int
    course_id: int
    lesson_id: int | None = None
    title: str = Field(..., max_length=255)
    type: str | None = None
    url: str
    uploaded_at: datetime

# DELETE Resource
class ResourceDelete(BaseModel):
    resource_id: int

# --- ATTENDANCE ---

# GET Attendance from a user and course
class AttendanceGet(BaseModel):
    attendance_id: int
    lesson_id: int
    student_id: int
    status: str
    recorded_at: datetime
    url: str | None = None # Optional isncase any dicument need to be added for the reason of Attendance
    uploaded_at: datetime   

# Create Attendance
class AttendanceCreate(BaseModel):
    lesson_id: int
    student_id: int
    status: str = Field(..., pattern="^(present|absent|late)$") # Attendance can be only present|absent|late
    url: str | None = None

# PUT Attendance
class AttendancePut(BaseModel):
    attendance_id: int
    lesson_id: int
    student_id: int
    status: str = Field(..., pattern="^(present|absent|late)$") # Attendance can be only present|absent|late
    url: str | None = None
    recorded_at: datetime
    uploaded_at: datetime

# DELETE Attendance
class AttendanceDelete(BaseModel):
    id: int