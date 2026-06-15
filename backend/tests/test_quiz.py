def test_create_quiz(client, teacher_headers):
    """Test creating a quiz"""
    # First create a course
    course_res = client.post("/courses/", json={
        "title": "Quiz Test Course",
        "description": "Course for quiz testing",
        "category": "Test",
        "difficulty_level": "beginner"
    }, headers=teacher_headers)
    course_id = course_res.json()["id"]

    # Create quiz
    res = client.post(f"/quiz/course/{course_id}", json={
        "title": "Test Quiz",
        "pass_marks": 2,
        "time_limit_minutes": 10
    }, headers=teacher_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test Quiz"
    print("✅ Quiz creation works!")

def test_add_question(client, teacher_headers):
    """Test adding a question to a quiz"""
    course_res = client.post("/courses/", json={
        "title": "Question Test Course",
        "description": "Course for question testing",
        "category": "Test",
        "difficulty_level": "beginner"
    }, headers=teacher_headers)
    course_id = course_res.json()["id"]

    quiz_res = client.post(f"/quiz/course/{course_id}", json={
        "title": "Question Test Quiz",
        "pass_marks": 1
    }, headers=teacher_headers)
    quiz_id = quiz_res.json()["id"]

    res = client.post(f"/quiz/{quiz_id}/questions", json={
        "question_text": "What is 2+2?",
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_option": "b",
        "marks": 1
    }, headers=teacher_headers)
    assert res.status_code == 200
    assert res.json()["question_text"] == "What is 2+2?"
    print("✅ Question creation works!")

def test_submit_quiz_correct(client, auth_headers, teacher_headers):
    """Test submitting a quiz with correct answers"""
    # Create course, quiz, question
    course_res = client.post("/courses/", json={
        "title": "Submit Test Course",
        "description": "Course for submit testing",
        "category": "Test",
        "difficulty_level": "beginner"
    }, headers=teacher_headers)
    course_id = course_res.json()["id"]

    quiz_res = client.post(f"/quiz/course/{course_id}", json={
        "title": "Submit Test Quiz",
        "pass_marks": 1
    }, headers=teacher_headers)
    quiz_id = quiz_res.json()["id"]

    q_res = client.post(f"/quiz/{quiz_id}/questions", json={
        "question_text": "What is Python?",
        "option_a": "A snake",
        "option_b": "A programming language",
        "option_c": "A database",
        "option_d": "An OS",
        "correct_option": "b",
        "marks": 1
    }, headers=teacher_headers)
    question_id = q_res.json()["id"]

    # Submit correct answer
    res = client.post(f"/quiz/{quiz_id}/submit", json={
        "answers": [{"question_id": question_id, "selected_option": "b"}]
    }, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["score"] == 1
    assert data["passed"] == True
    assert data["correct_count"] == 1
    print("✅ Quiz submission and grading works!")

def test_submit_quiz_wrong(client, auth_headers, teacher_headers):
    """Test submitting a quiz with wrong answers"""
    course_res = client.post("/courses/", json={
        "title": "Wrong Answer Course",
        "description": "Test",
        "category": "Test",
        "difficulty_level": "beginner"
    }, headers=teacher_headers)
    course_id = course_res.json()["id"]

    quiz_res = client.post(f"/quiz/course/{course_id}", json={
        "title": "Wrong Answer Quiz",
        "pass_marks": 1
    }, headers=teacher_headers)
    quiz_id = quiz_res.json()["id"]

    q_res = client.post(f"/quiz/{quiz_id}/questions", json={
        "question_text": "Capital of France?",
        "option_a": "London",
        "option_b": "Berlin",
        "option_c": "Paris",
        "option_d": "Rome",
        "correct_option": "c",
        "marks": 1
    }, headers=teacher_headers)
    question_id = q_res.json()["id"]

    # Submit wrong answer
    res = client.post(f"/quiz/{quiz_id}/submit", json={
        "answers": [{"question_id": question_id, "selected_option": "a"}]
    }, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["score"] == 0
    assert data["passed"] == False
    assert data["wrong_count"] == 1
    print("✅ Wrong answer detection works!")