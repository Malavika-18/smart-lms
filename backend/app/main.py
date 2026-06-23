from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import (
    auth, courses, quiz, recommendations,
    performance, analytics, chatbot, timelog, certificate
)
from app.seed import run_seed
import os

Base.metadata.create_all(bind=engine)
run_seed()

app = FastAPI(
    title="Smart LMS API",
    description="Smart Learning Management System using Data Science and AI",
    version="1.0.0"
)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:80"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(quiz.router)
app.include_router(recommendations.router)
app.include_router(performance.router)
app.include_router(analytics.router)
app.include_router(chatbot.router)
app.include_router(timelog.router)
app.include_router(certificate.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Smart LMS API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/admin/reset-db")
def reset_db():
    from app.database import Base, engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    run_seed()
    return {"message": "DB reset and re-seeded successfully!"}

@app.get("/setup-db")
def setup_db():
    """One-time DB setup for Render"""
    from app.database import engine
    from sqlalchemy import text
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE courses ADD COLUMN IF NOT EXISTS is_premium BOOLEAN DEFAULT FALSE"))
            conn.execute(text("ALTER TABLE courses ADD COLUMN IF NOT EXISTS price DECIMAL(10,2) DEFAULT 0.00"))
            conn.execute(text("ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS is_paid BOOLEAN DEFAULT FALSE"))
            conn.execute(text("ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS certificate_issued BOOLEAN DEFAULT FALSE"))
            conn.execute(text("ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS certificate_issued_at TIMESTAMP"))
            conn.execute(text("ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS quiz_best_score FLOAT DEFAULT 0.0"))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS time_logs (
                    id SERIAL PRIMARY KEY,
                    student_id INT REFERENCES users(id) ON DELETE CASCADE,
                    course_id INT REFERENCES courses(id) ON DELETE SET NULL,
                    page_name VARCHAR(100),
                    duration_seconds INT DEFAULT 0,
                    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    from app.seed import run_seed
    run_seed()
    return {"status": "success", "message": "DB setup and seeded!"} 