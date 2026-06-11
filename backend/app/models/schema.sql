CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('student', 'teacher', 'admin')) NOT NULL,
    profile_picture VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    teacher_id INT REFERENCES users(id) ON DELETE SET NULL,
    category VARCHAR(100),
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    thumbnail_url VARCHAR(255),
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    video_url VARCHAR(255),
    order_index INT,
    duration_minutes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES users(id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    progress_percent FLOAT DEFAULT 0.0,
    completed BOOLEAN DEFAULT FALSE,
    UNIQUE(student_id, course_id)
);
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    total_marks INT DEFAULT 0,
    pass_marks INT DEFAULT 0,
    time_limit_minutes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INT REFERENCES quizzes(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255),
    option_b VARCHAR(255),
    option_c VARCHAR(255),
    option_d VARCHAR(255),
    correct_option CHAR(1) CHECK (correct_option IN ('a','b','c','d')),
    marks INT DEFAULT 1
);
CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES users(id) ON DELETE CASCADE,
    quiz_id INT REFERENCES quizzes(id) ON DELETE CASCADE,
    score FLOAT,
    total_marks INT,
    passed BOOLEAN,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    due_date TIMESTAMP,
    total_marks INT DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE assignment_submissions (
    id SERIAL PRIMARY KEY,
    assignment_id INT REFERENCES assignments(id) ON DELETE CASCADE,
    student_id INT REFERENCES users(id) ON DELETE CASCADE,
    file_url VARCHAR(255),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    marks_obtained FLOAT,
    feedback TEXT,
    UNIQUE(assignment_id, student_id)
);
CREATE TABLE performance_logs (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES users(id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    login_count INT DEFAULT 0,
    time_spent_minutes INT DEFAULT 0,
    quiz_avg_score FLOAT,
    assignment_avg_score FLOAT,
    engagement_score FLOAT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE leaderboard (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES users(id) ON DELETE CASCADE,
    total_points INT DEFAULT 0,
    badges_earned TEXT[],
    rank INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);