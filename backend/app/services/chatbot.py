import random

RESPONSES = {
    "greeting": [
        "Hi there! 👋 I'm SmartBot, your AI learning assistant! How can I help you today?",
        "Hello! 😊 Ready to help you learn! What's on your mind?",
        "Hey! 🌟 Great to see you! What would you like to learn about today?"
    ],
    "quiz": [
        "📝 Quiz Tips:\n1. Read each question carefully\n2. Eliminate wrong answers first\n3. Don't spend too much time on one question\n4. Review your answers before submitting!\nYou've got this! 💪",
        "🎯 To improve quiz scores:\n• Review your course materials daily\n• Practice with past questions\n• Focus on topics where you scored low\n• Take notes while studying!",
        "💡 Before attempting a quiz:\n• Make sure you've completed all lessons\n• Take notes on key concepts\n• Get a good night's sleep\n• Stay calm and focused! 😊"
    ],
    "study": [
        "📚 Effective Study Tips:\n1. Use the Pomodoro Technique (25 min study, 5 min break)\n2. Create a distraction-free environment\n3. Summarize what you learned in your own words\n4. Teach concepts to someone else — it really helps!",
        "🧠 Smart Study Strategies:\n• Active recall — test yourself regularly\n• Spaced repetition — review material over time\n• Mind maps — visualize connections\n• Practice problems — apply what you learn!",
        "⏰ Time Management for Students:\n• Set a daily study schedule\n• Break big topics into smaller chunks\n• Prioritize difficult subjects first\n• Take regular breaks to stay fresh!"
    ],
    "ai_ml": [
        "🤖 AI vs ML:\n• AI (Artificial Intelligence) = Making machines think like humans\n• ML (Machine Learning) = Teaching machines to learn from data\n• ML is a subset of AI!\n\nExample: AI = self-driving car 🚗, ML = the model that learns to recognize roads!",
        "🧠 Machine Learning Types:\n1. Supervised Learning — learns from labeled data\n2. Unsupervised Learning — finds patterns in unlabeled data\n3. Reinforcement Learning — learns through rewards and penalties\n\nWhich one would you like to explore more? 😊"
    ],
    "programming": [
        "💻 Programming Best Practices:\n1. Write clean, readable code\n2. Comment your code well\n3. Break problems into smaller functions\n4. Test your code regularly\n5. Use version control (Git)!",
        "🐍 Python Tips:\n• Use meaningful variable names\n• Follow PEP 8 style guide\n• Use list comprehensions for clean code\n• Learn libraries like NumPy, Pandas for data science!\n• Practice daily on LeetCode or HackerRank! 💪"
    ],
    "motivation": [
        "💪 You're doing amazing! Remember:\n• Every expert was once a beginner\n• Progress > Perfection\n• Small steps every day lead to big results\n• Believe in yourself! 🌟",
        "🌟 Stay Motivated:\n• Set small, achievable daily goals\n• Celebrate every win, no matter how small\n• Surround yourself with positive learners\n• Remember WHY you started! 🎯",
        "🚀 Keep Going!\n• Consistency beats intensity\n• Learning is a journey, not a race\n• Every mistake is a lesson\n• You are capable of more than you know! ✨"
    ],
    "course": [
        "📖 To make the most of your courses:\n1. Complete lessons in order\n2. Take notes as you go\n3. Attempt all quizzes\n4. Revisit difficult concepts\n5. Apply what you learn practically!",
        "🎓 Course Success Tips:\n• Set a goal to complete one lesson per day\n• Engage in discussions with other students\n• Ask questions whenever you're stuck\n• Connect theory with real-world examples!"
    ],
    "performance": [
        "📈 To improve your performance:\n1. Review your quiz history regularly\n2. Focus on weak areas\n3. Re-attempt failed quizzes\n4. Track your progress weekly\n5. Set score targets for each quiz!",
        "🎯 Performance Improvement Plan:\n• Identify your weak topics from quiz results\n• Spend extra time on those topics\n• Practice with additional resources\n• Monitor your improvement over time! 📊"
    ],
    "leaderboard": [
        "🏆 Want to climb the leaderboard?\n1. Attempt more quizzes\n2. Score higher on each attempt\n3. Complete more courses\n4. Stay consistent every day\n5. Every point counts! 🌟",
        "🥇 Leaderboard Strategy:\n• Focus on accuracy over speed\n• Complete all available quizzes\n• Review mistakes and retry\n• A few points daily adds up fast! 💪"
    ],
    "python": [
        "🐍 Python is great for beginners!\nKey concepts to master:\n• Variables and Data Types\n• Loops and Conditions\n• Functions\n• Lists, Dicts, Tuples\n• OOP (Object-Oriented Programming)\n• Libraries: NumPy, Pandas, Scikit-learn",
        "💡 Learning Python Step by Step:\n1. Start with basic syntax\n2. Practice with small projects\n3. Learn data structures\n4. Explore libraries\n5. Build real projects!\n\nYou're already using Python for this LMS! 🎉"
    ],
    "data_science": [
        "📊 Data Science Roadmap:\n1. Learn Python basics\n2. Master NumPy & Pandas\n3. Data visualization (Matplotlib, Seaborn)\n4. Statistics & Probability\n5. Machine Learning (Scikit-learn)\n6. Deep Learning (TensorFlow/PyTorch)\n\nYou've got this! 🚀",
        "🔬 Data Science Skills:\n• Data Collection & Cleaning\n• Exploratory Data Analysis (EDA)\n• Feature Engineering\n• Model Building & Evaluation\n• Deployment\n\nThis LMS uses all of these! 🌟"
    ],
    "help": [
        "🤖 I can help you with:\n• 📝 Quiz tips and strategies\n• 📚 Study techniques\n• 💻 Programming concepts\n• 🤖 AI and Machine Learning\n• 📊 Data Science topics\n• 💪 Motivation and mindset\n• 🏆 Leaderboard strategies\n• 📖 Course guidance\n\nJust ask me anything! 😊"
    ],
    "default": [
        "🤔 That's an interesting question! I'm specialized in learning and academic topics. Could you ask me about:\n• Study tips\n• Quiz strategies\n• Programming\n• AI/ML concepts\n• Course guidance?",
        "😊 I'm here to help with your learning journey! Try asking me about study tips, quiz strategies, programming, or any academic topic!",
        "💡 Great question! While I may not have a specific answer for that, I can definitely help you with study strategies, course guidance, and technical concepts. What would you like to explore?"
    ]
}

def detect_intent(message: str) -> str:
    message_lower = message.lower()

    if any(word in message_lower for word in ["quiz", "test", "exam", "score", "marks", "grade", "attempt", "question", "answer", "pass", "fail"]):
        return "quiz"
    if any(word in message_lower for word in ["python", "pandas", "numpy", "scikit", "tensorflow", "pytorch", "flask", "fastapi", "django"]):
        return "python"
    if any(word in message_lower for word in ["data science", "data analysis", "dataset", "visualization", "statistics", "probability", "feature", "preprocessing", "eda"]):
        return "data_science"
    if any(word in message_lower for word in ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "neural", "algorithm", "model", "prediction", "classification", "regression", "clustering"]):
        return "ai_ml"
    if any(word in message_lower for word in ["code", "coding", "programming", "debug", "function", "variable", "loop", "syntax", "error", "bug", "software", "javascript", "react", "html", "css"]):
        return "programming"
    if any(word in message_lower for word in ["leaderboard", "rank", "points", "top", "position", "badge", "reward", "first place", "competition"]):
        return "leaderboard"
    if any(word in message_lower for word in ["performance", "progress", "improve", "better", "weak", "strength", "analytics", "track", "history", "result"]):
        return "performance"
    if any(word in message_lower for word in ["course", "lesson", "module", "enroll", "complete", "curriculum", "syllabus", "content", "material"]):
        return "course"
    if any(word in message_lower for word in ["motivat", "discouraged", "tired", "give up", "struggling", "hard", "difficult", "stress", "anxious", "worried", "inspire", "encourage"]):
        return "motivation"
    if any(word in message_lower for word in ["study", "learn", "memorize", "remember", "focus", "concentrate", "revision", "review", "notes", "tips", "technique", "strategy"]):
        return "study"
    if any(word in message_lower for word in ["help", "what can you do", "commands", "options", "features", "capabilities", "support"]):
        return "help"
    if any(word in message_lower for word in ["hi", "hello", "hey", "good morning", "good evening", "howdy", "greetings", "what's up", "sup"]):
        return "greeting"

    return "default"


def get_chatbot_response(
    message: str,
    conversation_history: list,
    student_name: str = "Student"
) -> str:
    intent = detect_intent(message)
    responses = RESPONSES.get(intent, RESPONSES["default"])
    response = random.choice(responses)

    if random.random() > 0.7:
        response = f"{student_name}, " + response[0].lower() + response[1:]

    return response