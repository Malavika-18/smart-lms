"""
Auto-seed: runs automatically when backend starts.
Skips if data already exists.
"""
from app.database import SessionLocal
from app.models.user import User
from app.models.course import Course, Lesson
from app.models.quiz import Quiz, Question
from app.utils.auth import hash_password

def run_seed():
    db = SessionLocal()
    try:
        # ── Skip if already seeded ──
        existing = db.query(Course).count()
        if existing >= 5:
            print(f"✅ Database already has {existing} courses. Skipping seed.")
            return

        print("🌱 Auto-seeding database...")

        # ── Create Teacher ──
        teacher = db.query(User).filter(
            User.email == "teacher@smartlms.com"
        ).first()

        if not teacher:
            teacher = User(
                full_name="Dr. Sarah Johnson",
                email="teacher@smartlms.com",
                password_hash=hash_password("teacher123"),
                role="teacher"
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            print("✅ Teacher account created")

        # ── Course Data ──
        COURSES = [
            {
                "title": "Python for Beginners",
                "description": "Learn Python from scratch. Covers variables, loops, functions, OOP and more.",
                "category": "Programming",
                "difficulty_level": "beginner",
                "lessons": [
                    {"title": "Introduction to Python", "content": "Python is a high-level language known for simplicity. Learn installation and your first program.", "duration_minutes": 20},
                    {"title": "Variables and Data Types", "content": "Learn integers, floats, strings, booleans, lists, and dictionaries.", "duration_minutes": 30},
                    {"title": "Loops and Functions", "content": "Master for loops, while loops, and reusable functions.", "duration_minutes": 35},
                ],
                "quizzes": [
                    {
                        "title": "Python Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is the correct way to print in Python?", "a": "print('Hello')", "b": "echo('Hello')", "c": "printf('Hello')", "d": "console.log('Hello')", "ans": "a"},
                            {"q": "Which data type is used for decimal numbers?", "a": "int", "b": "str", "c": "float", "d": "bool", "ans": "c"},
                            {"q": "How do you start a for loop in Python?", "a": "for i in range(10):", "b": "for (i=0;i<10;i++)", "c": "loop i from 0 to 10", "d": "foreach i in 10", "ans": "a"},
                            {"q": "What does len() do?", "a": "Returns length", "b": "Converts to int", "c": "Creates list", "d": "Prints output", "ans": "a"},
                            {"q": "Which keyword defines a function?", "a": "function", "b": "def", "c": "fun", "d": "define", "ans": "b"},
                        ]
                    }
                ]
            },
            {
                "title": "Machine Learning Fundamentals",
                "description": "Introduction to ML with supervised learning, model evaluation, and Scikit-learn.",
                "category": "Data Science",
                "difficulty_level": "intermediate",
                "lessons": [
                    {"title": "What is Machine Learning?", "content": "ML is a subset of AI. Learn supervised, unsupervised, and reinforcement learning.", "duration_minutes": 25},
                    {"title": "Supervised Learning", "content": "Linear Regression, Decision Trees, Random Forest, and SVM explained.", "duration_minutes": 45},
                    {"title": "Model Evaluation", "content": "Accuracy, precision, recall, F1-score, and cross-validation.", "duration_minutes": 40},
                ],
                "quizzes": [
                    {
                        "title": "ML Concepts Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is supervised learning?", "a": "Learning without labels", "b": "Learning with labeled data", "c": "Learning by rewards", "d": "Learning from clusters", "ans": "b"},
                            {"q": "Which algorithm is used for classification?", "a": "Linear Regression", "b": "K-Means", "c": "Random Forest", "d": "PCA", "ans": "c"},
                            {"q": "What does overfitting mean?", "a": "Model too simple", "b": "Performs well everywhere", "c": "Memorizes training data", "d": "Low accuracy", "ans": "c"},
                            {"q": "Purpose of train-test split?", "a": "Speed up training", "b": "Evaluate on unseen data", "c": "Reduce dataset", "d": "Clean data", "ans": "b"},
                            {"q": "Which metric measures classification?", "a": "MSE", "b": "RMSE", "c": "F1-Score", "d": "R-squared", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Web Development with React",
                "description": "Build modern web apps using React.js, hooks, routing, and REST APIs.",
                "category": "Web Development",
                "difficulty_level": "intermediate",
                "lessons": [
                    {"title": "React Fundamentals", "content": "JSX, components, props, and the Virtual DOM explained.", "duration_minutes": 30},
                    {"title": "State and Hooks", "content": "useState, useEffect, useContext, and custom hooks.", "duration_minutes": 40},
                    {"title": "React Router and APIs", "content": "Client-side routing and fetching data from REST APIs.", "duration_minutes": 35},
                ],
                "quizzes": [
                    {
                        "title": "React Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is JSX?", "a": "Database language", "b": "JavaScript XML syntax", "c": "CSS framework", "d": "Testing library", "ans": "b"},
                            {"q": "Which hook manages state?", "a": "useEffect", "b": "useContext", "c": "useState", "d": "useRef", "ans": "c"},
                            {"q": "What are React props?", "a": "Internal state", "b": "Database connections", "c": "Read-only inputs", "d": "CSS properties", "ans": "c"},
                            {"q": "useEffect is used for?", "a": "Managing state", "b": "Side effects", "c": "Creating components", "d": "Styling", "ans": "b"},
                            {"q": "Virtual DOM purpose?", "a": "Store data", "b": "Render HTML directly", "c": "Minimize DOM updates", "d": "Connect server", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Data Analysis with Pandas",
                "description": "Master data manipulation, cleaning, and visualization using Pandas.",
                "category": "Data Science",
                "difficulty_level": "beginner",
                "lessons": [
                    {"title": "Introduction to Pandas", "content": "DataFrames, Series, head(), tail(), info(), describe().", "duration_minutes": 25},
                    {"title": "Data Cleaning", "content": "Handle missing values, remove duplicates, fix data types.", "duration_minutes": 35},
                    {"title": "Data Visualization", "content": "Matplotlib and Seaborn for charts and graphs.", "duration_minutes": 30},
                ],
                "quizzes": [
                    {
                        "title": "Pandas Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is a Pandas DataFrame?", "a": "A Python list", "b": "2D labeled data structure", "c": "A neural network", "d": "A database", "ans": "b"},
                            {"q": "How to read CSV in Pandas?", "a": "pd.open_csv()", "b": "pd.load()", "c": "pd.read_csv()", "d": "pd.import_csv()", "ans": "c"},
                            {"q": "Which shows first 5 rows?", "a": "df.top()", "b": "df.first()", "c": "df.head()", "d": "df.start()", "ans": "c"},
                            {"q": "How to drop missing values?", "a": "df.remove_na()", "b": "df.dropna()", "c": "df.clean()", "d": "df.delete_null()", "ans": "b"},
                            {"q": "What does df.shape return?", "a": "Column names", "b": "Data types", "c": "Rows and columns", "d": "Statistics", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Database Design with SQL",
                "description": "Learn relational databases, SQL queries, joins, and PostgreSQL.",
                "category": "Database",
                "difficulty_level": "beginner",
                "lessons": [
                    {"title": "Introduction to SQL", "content": "CREATE, INSERT, SELECT, UPDATE, DELETE with examples.", "duration_minutes": 30},
                    {"title": "Joins and Relationships", "content": "INNER JOIN, LEFT JOIN, RIGHT JOIN, foreign keys.", "duration_minutes": 35},
                    {"title": "Advanced SQL", "content": "GROUP BY, HAVING, subqueries, indexes, transactions.", "duration_minutes": 40},
                ],
                "quizzes": [
                    {
                        "title": "SQL Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "Which command retrieves data?", "a": "INSERT", "b": "UPDATE", "c": "SELECT", "d": "DELETE", "ans": "c"},
                            {"q": "What does PRIMARY KEY do?", "a": "Encrypts data", "b": "Uniquely identifies rows", "c": "Links tables", "d": "Sorts data", "ans": "b"},
                            {"q": "Which JOIN returns matching rows?", "a": "LEFT JOIN", "b": "RIGHT JOIN", "c": "INNER JOIN", "d": "OUTER JOIN", "ans": "c"},
                            {"q": "What does GROUP BY do?", "a": "Sort results", "b": "Filter rows", "c": "Group by column", "d": "Join tables", "ans": "c"},
                            {"q": "What is a FOREIGN KEY?", "a": "Unique identifier", "b": "Key from another table", "c": "Encrypted field", "d": "An index", "ans": "b"},
                        ]
                    }
                ]
            },
            {
                "title": "Statistics for Data Science",
                "description": "Probability, distributions, hypothesis testing, and regression for data scientists.",
                "category": "Data Science",
                "difficulty_level": "beginner",
                "lessons": [
                    {"title": "Descriptive Statistics", "content": "Mean, median, mode, variance, standard deviation.", "duration_minutes": 25},
                    {"title": "Probability and Distributions", "content": "Normal, binomial, Poisson distributions and Bayes theorem.", "duration_minutes": 35},
                    {"title": "Hypothesis Testing", "content": "p-values, t-tests, chi-square, ANOVA explained.", "duration_minutes": 40},
                ],
                "quizzes": [
                    {
                        "title": "Statistics Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "Mean of [2,4,6,8]?", "a": "4", "b": "5", "c": "6", "d": "3", "ans": "b"},
                            {"q": "Standard deviation measures?", "a": "Central value", "b": "Spread around mean", "c": "Highest value", "d": "Sum", "ans": "b"},
                            {"q": "Normal distribution is called?", "a": "Skewed curve", "b": "Bell curve", "c": "Flat curve", "d": "Binomial curve", "ans": "b"},
                            {"q": "p-value represents?", "a": "Prediction accuracy", "b": "Probability by chance", "c": "Model performance", "d": "Data size", "ans": "b"},
                            {"q": "Median of [1,3,5,7,9]?", "a": "3", "b": "7", "c": "5", "d": "4", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Deep Learning with TensorFlow",
                "description": "Build neural networks using TensorFlow and Keras for real AI applications.",
                "category": "AI",
                "difficulty_level": "advanced",
                "lessons": [
                    {"title": "Neural Networks Basics", "content": "Neurons, activation functions, backpropagation, gradient descent.", "duration_minutes": 45},
                    {"title": "Convolutional Neural Networks", "content": "CNNs for image recognition, MNIST classifier.", "duration_minutes": 50},
                    {"title": "Model Training and Deployment", "content": "Callbacks, early stopping, saving and deploying models.", "duration_minutes": 40},
                ],
                "quizzes": [
                    {
                        "title": "Deep Learning Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is a neural network?", "a": "A database", "b": "Interconnected artificial neurons", "c": "A sorting algorithm", "d": "A web framework", "ans": "b"},
                            {"q": "Which activation outputs 0 or 1?", "a": "ReLU", "b": "Tanh", "c": "Sigmoid", "d": "Softmax", "ans": "c"},
                            {"q": "Backpropagation does?", "a": "Forward pass", "b": "Updates weights", "c": "Creates layers", "d": "Normalizes data", "ans": "b"},
                            {"q": "CNN stands for?", "a": "Connected Neural Node", "b": "Convolutional Neural Network", "c": "Computed Network", "d": "Clustered Network", "ans": "b"},
                            {"q": "Dropout layer prevents?", "a": "Slow training", "b": "Missing neurons", "c": "Overfitting", "d": "Data loss", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Natural Language Processing",
                "description": "Text preprocessing, sentiment analysis, and transformers using SpaCy and HuggingFace.",
                "category": "AI",
                "difficulty_level": "advanced",
                "lessons": [
                    {"title": "Text Preprocessing", "content": "Tokenization, stemming, lemmatization, TF-IDF.", "duration_minutes": 35},
                    {"title": "Sentiment Analysis", "content": "Naive Bayes and LSTM for sentiment classification.", "duration_minutes": 40},
                    {"title": "Transformers and BERT", "content": "Attention mechanism, fine-tuning BERT with HuggingFace.", "duration_minutes": 50},
                ],
                "quizzes": [
                    {
                        "title": "NLP Fundamentals Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "Tokenization means?", "a": "Encrypting text", "b": "Splitting into words", "c": "Translating text", "d": "Summarizing", "ans": "b"},
                            {"q": "TF-IDF measures?", "a": "Text length", "b": "Word importance", "c": "Sentence similarity", "d": "Grammar errors", "ans": "b"},
                            {"q": "Stemming reduces words to?", "a": "Prefixes", "b": "Root form", "c": "Translations", "d": "Counts", "ans": "b"},
                            {"q": "Sentiment analysis detects?", "a": "Text length", "b": "Emotion or opinion", "c": "Language type", "d": "Keywords", "ans": "b"},
                            {"q": "BERT stands for?", "a": "Basic Encoding", "b": "Bidirectional Encoder Representations from Transformers", "c": "Binary Encoding", "d": "Batch Encoded", "ans": "b"},
                        ]
                    }
                ]
            },
            {
                "title": "DevOps and Docker",
                "description": "Containerization, CI/CD pipelines, Docker, and cloud deployment essentials.",
                "category": "DevOps",
                "difficulty_level": "intermediate",
                "lessons": [
                    {"title": "Introduction to Docker", "content": "Containers, images, volumes, Dockerfile basics.", "duration_minutes": 35},
                    {"title": "Docker Compose", "content": "Multi-container apps with docker-compose.yml.", "duration_minutes": 30},
                    {"title": "CI/CD Pipelines", "content": "GitHub Actions for automated testing and deployment.", "duration_minutes": 40},
                ],
                "quizzes": [
                    {
                        "title": "Docker and DevOps Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is a Docker container?", "a": "Virtual machine", "b": "Lightweight isolated environment", "c": "Cloud server", "d": "Database", "ans": "b"},
                            {"q": "What is a Dockerfile?", "a": "DB config", "b": "Instructions to build image", "c": "Network config", "d": "Deploy script", "ans": "b"},
                            {"q": "docker-compose up does?", "a": "Stops containers", "b": "Builds and starts services", "c": "Removes containers", "d": "Lists images", "ans": "b"},
                            {"q": "CI stands for?", "a": "Container Integration", "b": "Continuous Integration", "c": "Cloud Infrastructure", "d": "Code Inspection", "ans": "b"},
                            {"q": "Kubernetes is used for?", "a": "Database management", "b": "Container orchestration", "c": "Version control", "d": "Network monitoring", "ans": "b"},
                        ]
                    }
                ]
            },
            {
                "title": "Git and Version Control",
                "description": "Master Git branching, merging, pull requests, and GitHub workflows.",
                "category": "Tools",
                "difficulty_level": "beginner",
                "lessons": [
                    {"title": "Git Basics", "content": "init, clone, add, commit, push, pull explained.", "duration_minutes": 25},
                    {"title": "Branching and Merging", "content": "Create branches, merge, resolve conflicts.", "duration_minutes": 30},
                    {"title": "GitHub Workflows", "content": "Pull requests, code reviews, GitHub Actions.", "duration_minutes": 35},
                ],
                "quizzes": [
                    {
                        "title": "Git Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "Which initializes a Git repo?", "a": "git start", "b": "git create", "c": "git init", "d": "git new", "ans": "c"},
                            {"q": "Which stages files?", "a": "git commit", "b": "git add", "c": "git push", "d": "git stage", "ans": "b"},
                            {"q": "git push does?", "a": "Downloads code", "b": "Saves locally", "c": "Uploads to remote", "d": "Creates branch", "ans": "c"},
                            {"q": "What is a branch?", "a": "Full project copy", "b": "Independent development line", "c": "Remote server", "d": "Commit history", "ans": "b"},
                            {"q": "git merge does?", "a": "Deletes branch", "b": "Combines branches", "c": "Creates repo", "d": "Reverts changes", "ans": "b"},
                        ]
                    }
                ]
            },
        ]

        # ── Insert Courses ──
        for course_data in COURSES:
            exists = db.query(Course).filter(
                Course.title == course_data["title"]
            ).first()
            if exists:
                continue

            course = Course(
                title=course_data["title"],
                description=course_data["description"],
                category=course_data["category"],
                difficulty_level=course_data["difficulty_level"],
                teacher_id=teacher.id,
                is_published=True
            )
            db.add(course)
            db.commit()
            db.refresh(course)

            for i, ld in enumerate(course_data["lessons"]):
                db.add(Lesson(
                    course_id=course.id,
                    title=ld["title"],
                    content=ld["content"],
                    order_index=i + 1,
                    duration_minutes=ld["duration_minutes"]
                ))
            db.commit()

            for qd in course_data["quizzes"]:
                quiz = Quiz(
                    course_id=course.id,
                    title=qd["title"],
                    pass_marks=qd["pass_marks"],
                    total_marks=len(qd["questions"]),
                    time_limit_minutes=15
                )
                db.add(quiz)
                db.commit()
                db.refresh(quiz)

                for q in qd["questions"]:
                    db.add(Question(
                        quiz_id=quiz.id,
                        question_text=q["q"],
                        option_a=q["a"],
                        option_b=q["b"],
                        option_c=q["c"],
                        option_d=q["d"],
                        correct_option=q["ans"],
                        marks=1
                    ))
                db.commit()

        total = db.query(Course).count()
        print(f"🎉 Seed complete! {total} courses ready.")

    except Exception as e:
        print(f"❌ Seed error: {e}")
        db.rollback()
    finally:
        db.close()