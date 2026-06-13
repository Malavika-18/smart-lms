from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    category = Column(String(100))
    difficulty_level = Column(String(20), default="beginner")
    thumbnail_url = Column(String(255), nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    teacher = relationship("User", foreign_keys=[teacher_id])
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    title = Column(String(200), nullable=False)
    content = Column(Text)
    video_url = Column(String(255), nullable=True)
    order_index = Column(Integer, default=0)
    duration_minutes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    course = relationship("Course", back_populates="lessons")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    progress_percent = Column(Float, default=0.0)
    completed = Column(Boolean, default=False)

    student = relationship("User", foreign_keys=[student_id])
    course = relationship("Course", back_populates="enrollments")