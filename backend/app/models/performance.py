from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class PerformanceLog(Base):
    __tablename__ = "performance_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    login_count = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    quiz_avg_score = Column(Float, default=0.0)
    assignment_avg_score = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("User", foreign_keys=[student_id])