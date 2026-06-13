from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import auth, courses, quiz

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart LMS API",
    description="Smart Learning Management System using Data Science and AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(quiz.router)

@app.get("/")
def root():
    return {"message": "Welcome to Smart LMS API", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}