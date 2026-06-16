from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import auth, courses, quiz, recommendations, performance, analytics, chatbot
from app.seed import run_seed
import os

Base.metadata.create_all(bind=engine)

# Auto-seed on startup
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

@app.get("/")
def root():
    return {"message": "Welcome to Smart LMS API", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}