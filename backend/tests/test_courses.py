def test_get_courses_empty(client):
    """Test getting courses when none exist"""
    res = client.get("/courses/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    print("✅ Get courses works!")

def test_create_course_as_teacher(client, teacher_headers):
    """Test creating a course as a teacher"""
    res = client.post("/courses/", json={
        "title": "Test Course",
        "description": "A test course",
        "category": "Testing",
        "difficulty_level": "beginner"
    }, headers=teacher_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test Course"
    assert data["is_published"] == False
    print("✅ Course creation works!")

def test_create_course_as_student_fails(client, auth_headers):
    """Test that students cannot create courses"""
    res = client.post("/courses/", json={
        "title": "Unauthorized Course",
        "description": "Should fail",
        "category": "Test",
        "difficulty_level": "beginner"
    }, headers=auth_headers)
    assert res.status_code == 403
    print("✅ Student course creation blocked correctly!")

def test_enroll_in_course(client, auth_headers, teacher_headers):
    """Test enrolling in a course"""
    # Create and publish course
    course_res = client.post("/courses/", json={
        "title": "Enroll Test Course",
        "description": "For enrollment testing",
        "category": "Test",
        "difficulty_level": "beginner"
    }, headers=teacher_headers)
    course_id = course_res.json()["id"]

    # Publish it
    client.put(f"/courses/{course_id}",
        json={"is_published": True},
        headers=teacher_headers
    )

    # Enroll as student
    res = client.post(
        f"/courses/{course_id}/enroll",
        headers=auth_headers
    )
    assert res.status_code == 200
    assert res.json()["course_id"] == course_id
    print("✅ Course enrollment works!")

def test_double_enrollment_fails(client, auth_headers, teacher_headers):
    """Test that enrolling twice fails"""
    course_res = client.post("/courses/", json={
        "title": "Double Enroll Test",
        "description": "Test",
        "category": "Test",
        "difficulty_level": "beginner"
    }, headers=teacher_headers)
    course_id = course_res.json()["id"]

    client.post(f"/courses/{course_id}/enroll", headers=auth_headers)
    res = client.post(f"/courses/{course_id}/enroll", headers=auth_headers)
    assert res.status_code == 400
    print("✅ Double enrollment prevention works!")