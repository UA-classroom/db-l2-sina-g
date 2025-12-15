# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure

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

