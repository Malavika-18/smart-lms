from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.quiz import QuizAttempt
from app.models.course import Enrollment, Course
from app.ml.performance_predictor import predictor
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/performance", tags=["Performance"])

@router.get("/predict/{course_id}")
def predict_performance(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict student performance for a specific course"""
    result = predictor.predict(
        student_id=current_user.id,
        course_id=course_id,
        db=db
    )
    return result

@router.get("/summary")
def get_performance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overall performance summary for the student"""

    # Get all quiz attempts
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == current_user.id
    ).all()

    # Get all enrollments
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id
    ).all()

    # Calculate stats
    total_attempts = len(attempts)
    passed = sum(1 for a in attempts if a.passed)
    failed = total_attempts - passed

    avg_score = 0.0
    if attempts:
        scores = [
            (a.score / a.total_marks * 100)
            for a in attempts
            if a.total_marks and a.total_marks > 0
        ]
        avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    return {
        "student_id": current_user.id,
        "student_name": current_user.full_name,
        "total_courses_enrolled": len(enrollments),
        "total_quiz_attempts": total_attempts,
        "quizzes_passed": passed,
        "quizzes_failed": failed,
        "average_score": avg_score,
        "pass_rate": round((passed / total_attempts * 100), 1) if total_attempts > 0 else 0.0,
    }

@router.get("/history")
def get_attempt_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed quiz attempt history"""
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == current_user.id
    ).order_by(QuizAttempt.attempted_at.desc()).all()

    return [
        {
            "quiz_id": a.quiz_id,
            "score": a.score,
            "total_marks": a.total_marks,
            "passed": a.passed,
            "percentage": round((a.score / a.total_marks * 100), 1)
                if a.total_marks and a.total_marks > 0 else 0,
            "attempted_at": a.attempted_at
        }
        for a in attempts
    ]