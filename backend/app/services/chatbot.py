from app.config import settings

# Try Groq first, fallback to rule-based
try:
    from groq import Groq
    groq_client = Groq(api_key=settings.GROQ_API_KEY)
    GROQ_AVAILABLE = bool(settings.GROQ_API_KEY)
except Exception:
    GROQ_AVAILABLE = False

import random

SYSTEM_PROMPT = """You are SmartBot, an AI learning assistant for Smart LMS 
— an intelligent Learning Management System built with React, FastAPI, and Python.

You help students with:
- Understanding course concepts (Python, ML, React, SQL, Statistics, NLP, Docker, Git)
- Explaining quiz answers and solutions
- Study tips and learning strategies  
- Motivation and encouragement
- Career guidance in tech and data science
- Debugging code and technical questions

Guidelines:
- Be friendly, encouraging, and supportive
- Keep responses concise (3-5 sentences max unless code is needed)
- Use emojis to make responses engaging
- For code questions, provide short working examples
- Always end with an encouraging note for students
- If asked about something unrelated to learning/tech, politely redirect
"""

# Rule-based fallback responses
RESPONSES = {
    "greeting": [
        "Hi there! 👋 I'm SmartBot, your AI learning assistant! How can I help you today?",
        "Hello! 😊 Ready to help you learn! What's on your mind?",
        "Hey! 🌟 Great to see you! What would you like to learn about today?"
    ],
    "quiz": [
        "📝 Quiz Tips:\n1. Read each question carefully\n2. Eliminate wrong answers first\n3. Don't spend too much time on one question\n4. Review your answers before submitting!\nYou've got this! 💪",
        "🎯 To improve quiz scores:\n• Review course materials daily\n• Practice with past questions\n• Focus on topics where you scored low\n• Take notes while studying!",
    ],
    "study": [
        "📚 Effective Study Tips:\n1. Use the Pomodoro Technique (25 min study, 5 min break)\n2. Create a distraction-free environment\n3. Summarize in your own words\n4. Teach concepts to someone else!",
        "🧠 Smart Study Strategies:\n• Active recall — test yourself regularly\n• Spaced repetition — review over time\n• Mind maps — visualize connections\n• Practice problems — apply what you learn!",
    ],
    "motivation": [
        "💪 You're doing amazing! Every expert was once a beginner. Progress > Perfection. Keep going! 🌟",
        "🚀 Stay consistent! Small steps every day lead to big results. Believe in yourself! ✨",
    ],
    "default": [
        "🤔 Great question! I'm here to help with your learning journey. Try asking about study tips, quiz strategies, programming, or AI/ML concepts!",
        "😊 I'm your Smart LMS learning assistant! Ask me about courses, study strategies, or any tech topic! 💡"
    ]
}

def detect_intent(message: str) -> str:
    msg = message.lower()
    if any(w in msg for w in ["hi", "hello", "hey", "good morning", "good evening"]):
        return "greeting"
    if any(w in msg for w in ["quiz", "test", "exam", "score", "marks", "grade"]):
        return "quiz"
    if any(w in msg for w in ["study", "learn", "memorize", "focus", "tips", "strategy"]):
        return "study"
    if any(w in msg for w in ["motivat", "discouraged", "tired", "give up", "struggling", "hard"]):
        return "motivation"
    return "default"

def get_groq_response(message: str, conversation_history: list, student_name: str) -> str:
    """Get response from Groq AI"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add conversation history (last 10 messages)
    for msg in conversation_history[-10:]:
        if msg.get("role") in ["user", "assistant"] and msg.get("content"):
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # Add current message
    messages.append({
        "role": "user",
        "content": f"[Student: {student_name}] {message}"
    })

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Free model on Groq
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content

def get_chatbot_response(
    message: str,
    conversation_history: list,
    student_name: str = "Student"
) -> str:
    """Main function — uses Groq if available, else rule-based"""

    if GROQ_AVAILABLE:
        try:
            return get_groq_response(message, conversation_history, student_name)
        except Exception as e:
            print(f"Groq error: {e} — falling back to rule-based")

    # Fallback to rule-based
    intent = detect_intent(message)
    responses = RESPONSES.get(intent, RESPONSES["default"])
    response = random.choice(responses)
    if random.random() > 0.7:
        response = f"{student_name}, " + response[0].lower() + response[1:]
    return response