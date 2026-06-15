from app.services.chatbot import detect_intent, get_chatbot_response

def test_greeting_intent():
    assert detect_intent("hi") == "greeting"
    assert detect_intent("hello there") == "greeting"
    assert detect_intent("hey") == "greeting"
    print("✅ Greeting intent detection works!")

def test_quiz_intent():
    assert detect_intent("how to improve quiz scores") == "quiz"
    assert detect_intent("I failed my test") == "quiz"
    assert detect_intent("quiz tips please") == "quiz"
    print("✅ Quiz intent detection works!")

def test_study_intent():
    assert detect_intent("how to study effectively") == "study"
    assert detect_intent("study tips") == "study"
    assert detect_intent("help me memorize things") == "study"
    print("✅ Study intent detection works!")

def test_ai_ml_intent():
    assert detect_intent("what is machine learning") == "ai_ml"
    assert detect_intent("explain AI to me") == "ai_ml"
    assert detect_intent("difference between AI and ML") == "ai_ml"
    print("✅ AI/ML intent detection works!")

def test_motivation_intent():
    assert detect_intent("I want to give up") == "motivation"
    assert detect_intent("feeling discouraged") == "motivation"
    assert detect_intent("this is too hard") == "motivation"
    print("✅ Motivation intent detection works!")

def test_python_intent():
    assert detect_intent("python tips") == "python"
    assert detect_intent("how to use pandas") == "python"
    print("✅ Python intent detection works!")

def test_default_intent():
    assert detect_intent("what is the weather today") == "default"
    assert detect_intent("random gibberish xyz") == "default"
    print("✅ Default fallback works!")

def test_response_is_string():
    response = get_chatbot_response("hello", [], "Test Student")
    assert isinstance(response, str)
    assert len(response) > 0
    print("✅ Chatbot returns valid response!")

def test_chatbot_api(client, auth_headers):
    """Test chatbot API endpoint"""
    res = client.post("/chatbot/chat", json={
        "message": "hello",
        "history": []
    }, headers=auth_headers)
    assert res.status_code == 200
    assert "response" in res.json()
    print("✅ Chatbot API endpoint works!")

def test_suggestions_api(client, auth_headers):
    """Test suggestions endpoint"""
    res = client.get("/chatbot/suggestions", headers=auth_headers)
    assert res.status_code == 200
    assert "suggestions" in res.json()
    assert len(res.json()["suggestions"]) > 0
    print("✅ Suggestions API works!")