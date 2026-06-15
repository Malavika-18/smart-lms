from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.models.user import User
from app.services.chatbot import get_chatbot_response
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    role: str = "assistant"

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Send a message to the AI chatbot"""
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in request.history
    ]

    response = get_chatbot_response(
        message=request.message,
        conversation_history=history,
        student_name=current_user.full_name
    )

    return ChatResponse(response=response)

@router.get("/suggestions")
def get_suggestions(current_user: User = Depends(get_current_user)):
    """Get suggested questions for the chatbot"""
    return {
        "suggestions": [
            "How do I study effectively for exams? 📚",
            "Explain the concept of machine learning 🤖",
            "What are good programming practices? 💻",
            "How can I improve my quiz scores? 📈",
            "Give me tips for staying motivated 💪",
            "What is the difference between AI and ML? 🧠",
        ]
    }