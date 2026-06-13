from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.ml.recommendation import recommendation_engine
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/")
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AI-powered course recommendations for current student"""
    recommendations = recommendation_engine.get_recommendations(
        student_id=current_user.id,
        db=db,
        top_n=5
    )
    return {
        "student_id": current_user.id,
        "student_name": current_user.full_name,
        "recommendations": recommendations,
        "algorithm": "hybrid_content_collaborative"
    }

@router.get("/collaborative")
def get_collaborative_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get collaborative filtering recommendations"""
    recommendations = recommendation_engine.get_collaborative_recommendations(
        student_id=current_user.id,
        db=db,
        top_n=5
    )
    return {
        "student_id": current_user.id,
        "recommendations": recommendations,
        "algorithm": "collaborative_filtering"
    }

@router.get("/popular")
def get_popular_courses(db: Session = Depends(get_db)):
    """Get most popular courses by enrollment count"""
    from app.models.course import Course, Enrollment
    from sqlalchemy import func

    popular = db.query(
        Course,
        func.count(Enrollment.id).label("enrollment_count")
    ).join(
        Enrollment, Course.id == Enrollment.course_id, isouter=True
    ).filter(
        Course.is_published == True
    ).group_by(Course.id).order_by(
        func.count(Enrollment.id).desc()
    ).limit(5).all()

    return [
        {
            "id": course.id,
            "title": course.title,
            "category": course.category,
            "difficulty_level": course.difficulty_level,
            "enrollment_count": count
        }
        for course, count in popular
    ]