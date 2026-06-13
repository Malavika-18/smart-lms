from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    title = Column(String(200), nullable=False)
    total_marks = Column(Integer, default=0)
    pass_marks = Column(Integer, default=0)
    time_limit_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("Question", back_populates="quiz", cascade="all, delete")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    question_text = Column(Text, nullable=False)
    option_a = Column(String(255))
    option_b = Column(String(255))
    option_c = Column(String(255))
    option_d = Column(String(255))
    correct_option = Column(CHAR(1))
    marks = Column(Integer, default=1)

    quiz = relationship("Quiz", back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    score = Column(Float, nullable=True)
    total_marks = Column(Integer, nullable=True)
    passed = Column(Boolean, nullable=True)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    quiz = relationship("Quiz", back_populates="attempts")
    student = relationship("User", foreign_keys=[student_id])