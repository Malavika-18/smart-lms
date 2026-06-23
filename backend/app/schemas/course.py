from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = "beginner"
    thumbnail_url: Optional[str] = None
    is_premium: Optional[bool] = False
    price: Optional[float] = 0.00

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    is_published: Optional[bool] = None
    is_premium: Optional[bool] = None
    price: Optional[float] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    difficulty_level: Optional[str]
    thumbnail_url: Optional[str]
    is_published: bool
    is_premium: bool
    price: float
    teacher_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class LessonCreate(BaseModel):
    title: str
    content: Optional[str] = None
    video_url: Optional[str] = None
    order_index: Optional[int] = 0
    duration_minutes: Optional[int] = 0

class LessonResponse(BaseModel):
    id: int
    course_id: int
    title: str
    content: Optional[str]
    video_url: Optional[str]
    order_index: int
    duration_minutes: int

    class Config:
        from_attributes = True

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    progress_percent: float
    completed: bool
    is_paid: bool
    certificate_issued: bool
    certificate_issued_at: Optional[datetime]
    quiz_best_score: float
    enrolled_at: datetime

    class Config:
        from_attributes = True