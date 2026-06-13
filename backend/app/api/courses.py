from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.course import Course, Lesson, Enrollment
from app.models.user import User
from app.schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse,
    LessonCreate, LessonResponse, EnrollmentResponse
)
from app.utils.dependencies import get_current_user, require_teacher

router = APIRouter(prefix="/courses", tags=["Courses"])

# Get all published courses
@router.get("/", response_model=List[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(Course).filter(Course.is_published == True).all()

# Get single course
@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Create course (teachers only)
@router.post("/", response_model=CourseResponse)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    new_course = Course(
        **course_data.model_dump(),
        teacher_id=current_user.id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# Update course (teacher who owns it)
@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course

# Delete course
@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

# Add lesson to course
@router.post("/{course_id}/lessons", response_model=LessonResponse)
def add_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_lesson = Lesson(course_id=course_id, **lesson_data.model_dump())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

# Get lessons for a course
@router.get("/{course_id}/lessons", response_model=List[LessonResponse])
def get_lessons(course_id: int, db: Session = Depends(get_db)):
    return db.query(Lesson).filter(
        Lesson.course_id == course_id
    ).order_by(Lesson.order_index).all()

# Enroll in a course
@router.post("/{course_id}/enroll", response_model=EnrollmentResponse)
def enroll_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")

    enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

# Get my enrollments
@router.get("/my/enrollments", response_model=List[EnrollmentResponse])
def my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id
    ).all()