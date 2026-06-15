def test_register_student(client):
    """Test student registration"""
    res = client.post("/auth/register", json={
        "full_name": "New Student",
        "email": "newstudent@test.com",
        "password": "password123",
        "role": "student"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["role"] == "student"
    assert data["user"]["email"] == "newstudent@test.com"
    print("✅ Student registration works!")

def test_register_duplicate_email(client):
    """Test that duplicate emails are rejected"""
    client.post("/auth/register", json={
        "full_name": "Student One",
        "email": "duplicate@test.com",
        "password": "password123",
        "role": "student"
    })
    res = client.post("/auth/register", json={
        "full_name": "Student Two",
        "email": "duplicate@test.com",
        "password": "password456",
        "role": "student"
    })
    assert res.status_code == 400
    assert "already registered" in res.json()["detail"]
    print("✅ Duplicate email check works!")

def test_login_success(client):
    """Test successful login"""
    client.post("/auth/register", json={
        "full_name": "Login Test",
        "email": "logintest@test.com",
        "password": "test1234",
        "role": "student"
    })
    res = client.post("/auth/login", json={
        "email": "logintest@test.com",
        "password": "test1234"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()
    print("✅ Login works!")

def test_login_wrong_password(client):
    """Test login with wrong password"""
    client.post("/auth/register", json={
        "full_name": "Wrong Pass",
        "email": "wrongpass@test.com",
        "password": "correctpass",
        "role": "student"
    })
    res = client.post("/auth/login", json={
        "email": "wrongpass@test.com",
        "password": "wrongpass"
    })
    assert res.status_code == 401
    print("✅ Wrong password rejection works!")

def test_login_nonexistent_user(client):
    """Test login with email that doesn't exist"""
    res = client.post("/auth/login", json={
        "email": "nobody@test.com",
        "password": "password123"
    })
    assert res.status_code == 401
    print("✅ Nonexistent user rejection works!")