from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.quiz import Quiz, Question, QuizAttempt
from app.models.user import User
from app.schemas.quiz import (
    QuizCreate, QuizResponse, QuizWithQuestions,
    QuestionCreate, QuestionResponse,
    QuizSubmission, QuizResult
)
from app.utils.dependencies import get_current_user, require_teacher

router = APIRouter(prefix="/quiz", tags=["Quiz"])

# Create a quiz (teacher only)
@router.post("/course/{course_id}", response_model=QuizResponse)
def create_quiz(
    course_id: int,
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    new_quiz = Quiz(
        course_id=course_id,
        title=quiz_data.title,
        pass_marks=quiz_data.pass_marks,
        time_limit_minutes=quiz_data.time_limit_minutes,
        total_marks=0
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz

# Add question to quiz
@router.post("/{quiz_id}/questions", response_model=QuestionResponse)
def add_question(
    quiz_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    new_question = Question(quiz_id=quiz_id, **question_data.model_dump())
    db.add(new_question)

    # Update total marks
    quiz.total_marks += question_data.marks
    db.commit()
    db.refresh(new_question)
    return new_question

# Get quiz with questions (for students to attempt)
@router.get("/{quiz_id}", response_model=QuizWithQuestions)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

# Get all quizzes for a course
@router.get("/course/{course_id}", response_model=List[QuizResponse])
def get_course_quizzes(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Quiz).filter(Quiz.course_id == course_id).all()

# Submit quiz answers and get result
@router.post("/{quiz_id}/submit", response_model=QuizResult)
def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Auto-grade answers
    score = 0
    correct_count = 0
    wrong_count = 0

    for answer in submission.answers:
        question = db.query(Question).filter(
            Question.id == answer.question_id,
            Question.quiz_id == quiz_id
        ).first()
        if question:
            if answer.selected_option.lower() == question.correct_option.lower():
                score += question.marks
                correct_count += 1
            else:
                wrong_count += 1

    passed = score >= quiz.pass_marks
    percentage = (score / quiz.total_marks * 100) if quiz.total_marks > 0 else 0

    # Save attempt
    attempt = QuizAttempt(
        student_id=current_user.id,
        quiz_id=quiz_id,
        score=score,
        total_marks=quiz.total_marks,
        passed=passed
    )
    db.add(attempt)
    db.commit()

    return QuizResult(
        quiz_id=quiz_id,
        score=score,
        total_marks=quiz.total_marks,
        passed=passed,
        correct_count=correct_count,
        wrong_count=wrong_count,
        percentage=round(percentage, 2)
    )

# Get my quiz attempts
@router.get("/my/attempts")
def my_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == current_user.id
    ).all()
    return attempts