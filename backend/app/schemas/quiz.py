from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class QuestionCreate(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    marks: Optional[int] = 1

class QuestionResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    marks: int

    class Config:
        from_attributes = True

class QuizCreate(BaseModel):
    title: str
    pass_marks: Optional[int] = 0
    time_limit_minutes: Optional[int] = None

class QuizResponse(BaseModel):
    id: int
    course_id: int
    title: str
    total_marks: int
    pass_marks: int
    time_limit_minutes: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class QuizWithQuestions(QuizResponse):
    questions: List[QuestionResponse] = []

class StudentAnswer(BaseModel):
    question_id: int
    selected_option: str

class QuizSubmission(BaseModel):
    answers: List[StudentAnswer]

class QuizResult(BaseModel):
    quiz_id: int
    score: float
    total_marks: int
    passed: bool
    correct_count: int
    wrong_count: int
    percentage: float