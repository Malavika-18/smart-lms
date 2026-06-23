from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.course import Course, Enrollment
from app.models.quiz import QuizAttempt, Quiz
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/certificate", tags=["Certificate"])

PASSING_SCORE = 70.0  # 70% minimum to get certificate

@router.get("/check/{course_id}")
def check_certificate_eligibility(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if student is eligible for certificate"""

    # Check enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()

    if not enrollment:
        return {
            "eligible": False,
            "reason": "You are not enrolled in this course",
            "certificate_issued": False
        }

    # Already has certificate
    if enrollment.certificate_issued:
        return {
            "eligible": True,
            "certificate_issued": True,
            "issued_at": enrollment.certificate_issued_at,
            "quiz_best_score": enrollment.quiz_best_score,
            "reason": "Certificate already issued!"
        }

    # Check quiz score
    course_quizzes = db.query(Quiz).filter(
        Quiz.course_id == course_id
    ).all()

    if not course_quizzes:
        return {
            "eligible": False,
            "reason": "No quizzes found for this course",
            "certificate_issued": False
        }

    # Find best quiz score for this course
    best_score = 0.0
    for quiz in course_quizzes:
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.student_id == current_user.id,
            QuizAttempt.quiz_id == quiz.id
        ).all()

        for attempt in attempts:
            if attempt.total_marks and attempt.total_marks > 0:
                score_pct = (attempt.score / attempt.total_marks) * 100
                best_score = max(best_score, score_pct)

    # Check eligibility conditions
    lessons_viewed = enrollment.progress_percent >= 100.0
    quiz_passed = best_score >= PASSING_SCORE

    if not quiz_passed:
        return {
            "eligible": False,
            "certificate_issued": False,
            "quiz_best_score": round(best_score, 1),
            "required_score": PASSING_SCORE,
            "reason": f"You need {PASSING_SCORE}% in quiz. Your best: {round(best_score, 1)}%",
            "lessons_viewed": lessons_viewed,
            "quiz_passed": False
        }

    return {
        "eligible": True,
        "certificate_issued": False,
        "quiz_best_score": round(best_score, 1),
        "required_score": PASSING_SCORE,
        "reason": "You are eligible! Generate your certificate.",
        "lessons_viewed": lessons_viewed,
        "quiz_passed": True
    }


@router.post("/generate/{course_id}")
def generate_certificate(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate certificate after checking eligibility"""

    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()

    if not enrollment:
        raise HTTPException(status_code=400, detail="Not enrolled")

    # Check quiz score
    course_quizzes = db.query(Quiz).filter(
        Quiz.course_id == course_id
    ).all()

    best_score = 0.0
    for quiz in course_quizzes:
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.student_id == current_user.id,
            QuizAttempt.quiz_id == quiz.id
        ).all()
        for attempt in attempts:
            if attempt.total_marks and attempt.total_marks > 0:
                score_pct = (attempt.score / attempt.total_marks) * 100
                best_score = max(best_score, score_pct)

    if best_score < PASSING_SCORE:
        raise HTTPException(
            status_code=400,
            detail=f"Need {PASSING_SCORE}% score. Your best: {round(best_score, 1)}%"
        )

    # Issue certificate
    enrollment.certificate_issued = True
    enrollment.certificate_issued_at = datetime.utcnow()
    enrollment.quiz_best_score = round(best_score, 1)
    enrollment.completed = True
    enrollment.progress_percent = 100.0
    db.commit()

    return {
        "success": True,
        "student_name": current_user.full_name,
        "course_title": course.title,
        "quiz_score": round(best_score, 1),
        "issued_at": enrollment.certificate_issued_at,
        "certificate_id": f"SLMS-{current_user.id:04d}-{course_id:04d}-{datetime.utcnow().year}"
    }


@router.get("/my-certificates")
def get_my_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all certificates earned by student"""
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.certificate_issued == True
    ).all()

    certificates = []
    for e in enrollments:
        course = db.query(Course).filter(Course.id == e.course_id).first()
        if course:
            certificates.append({
                "certificate_id": f"SLMS-{current_user.id:04d}-{e.course_id:04d}-{e.certificate_issued_at.year if e.certificate_issued_at else 2024}",
                "course_id": course.id,
                "course_title": course.title,
                "category": course.category,
                "difficulty_level": course.difficulty_level,
                "quiz_score": e.quiz_best_score,
                "issued_at": e.certificate_issued_at,
                "student_name": current_user.full_name
            })

    return certificates