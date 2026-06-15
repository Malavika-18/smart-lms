from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.quiz import QuizAttempt
from app.models.course import Enrollment, Course
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """Get top students by quiz performance"""

    # Get all students with their quiz stats
    students = db.query(User).filter(User.role == "student").all()

    leaderboard = []
    for student in students:
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.student_id == student.id
        ).all()

        if not attempts:
            total_points = 0
            avg_score = 0.0
        else:
            total_points = sum(
                int(a.score) for a in attempts if a.score
            )
            scores = [
                (a.score / a.total_marks * 100)
                for a in attempts
                if a.total_marks and a.total_marks > 0
            ]
            avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

        enrollments = db.query(Enrollment).filter(
            Enrollment.student_id == student.id
        ).count()

        leaderboard.append({
            "student_id": student.id,
            "full_name": student.full_name,
            "total_points": total_points,
            "avg_score": avg_score,
            "courses_enrolled": enrollments,
            "quiz_attempts": len(attempts)
        })

    # Sort by total points descending
    leaderboard.sort(key=lambda x: x["total_points"], reverse=True)

    # Add rank
    for i, entry in enumerate(leaderboard):
        entry["rank"] = i + 1

    return leaderboard[:10]


@router.get("/overview")
def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get complete dashboard overview for current student"""

    # Quiz stats
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == current_user.id
    ).order_by(QuizAttempt.attempted_at.desc()).all()

    total_points = sum(int(a.score) for a in attempts if a.score)
    passed = sum(1 for a in attempts if a.passed)
    avg_score = 0.0
    if attempts:
        scores = [
            (a.score / a.total_marks * 100)
            for a in attempts
            if a.total_marks and a.total_marks > 0
        ]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

    # Enrolled courses with details
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id
    ).all()

    enrolled_courses = []
    for e in enrollments:
        course = db.query(Course).filter(Course.id == e.course_id).first()
        if course:
            enrolled_courses.append({
                "course_id": course.id,
                "title": course.title,
                "category": course.category,
                "difficulty_level": course.difficulty_level,
                "progress_percent": e.progress_percent,
                "completed": e.completed
            })

    # Recent quiz attempts
    recent_attempts = []
    for a in attempts[:5]:
        recent_attempts.append({
            "quiz_id": a.quiz_id,
            "score": a.score,
            "total_marks": a.total_marks,
            "passed": a.passed,
            "percentage": round(
                (a.score / a.total_marks * 100), 1
            ) if a.total_marks and a.total_marks > 0 else 0,
            "attempted_at": a.attempted_at
        })

    # Get leaderboard rank
    all_students = db.query(User).filter(User.role == "student").all()
    student_points = {}
    for s in all_students:
        s_attempts = db.query(QuizAttempt).filter(
            QuizAttempt.student_id == s.id
        ).all()
        student_points[s.id] = sum(
            int(a.score) for a in s_attempts if a.score
        )

    sorted_ids = sorted(
        student_points.keys(),
        key=lambda x: student_points[x],
        reverse=True
    )
    rank = sorted_ids.index(current_user.id) + 1 if current_user.id in sorted_ids else "-"

    return {
        "student": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role
        },
        "stats": {
            "total_points": total_points,
            "avg_score": avg_score,
            "quizzes_passed": passed,
            "total_attempts": len(attempts),
            "courses_enrolled": len(enrollments),
            "leaderboard_rank": rank
        },
        "enrolled_courses": enrolled_courses,
        "recent_attempts": recent_attempts
    }