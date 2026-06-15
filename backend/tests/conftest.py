import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use a separate test database
TEST_DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/smart_lms_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Create test client"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    """Register and login a test student, return auth headers"""
    # Register
    client.post("/auth/register", json={
        "full_name": "Test Student",
        "email": "teststudent@test.com",
        "password": "test1234",
        "role": "student"
    })
    # Login
    res = client.post("/auth/login", json={
        "email": "teststudent@test.com",
        "password": "test1234"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def teacher_headers(client):
    """Register and login a test teacher, return auth headers"""
    client.post("/auth/register", json={
        "full_name": "Test Teacher",
        "email": "testteacher@test.com",
        "password": "test1234",
        "role": "teacher"
    })
    res = client.post("/auth/login", json={
        "email": "testteacher@test.com",
        "password": "test1234"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}