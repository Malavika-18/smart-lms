"""
Auto-seed: runs automatically when backend starts.
Includes real YouTube videos and GeeksForGeeks links.
"""
from app.database import SessionLocal
from app.models.user import User
from app.models.course import Course, Lesson
from app.models.quiz import Quiz, Question
from app.utils.auth import hash_password

def run_seed():
    db = SessionLocal()
    try:
        existing = db.query(Course).count()
        if existing >= 5:
            print(f"✅ Database already has {existing} courses. Skipping seed.")
            return

        print("🌱 Auto-seeding database with real content...")

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

        COURSES = [
            {
                "title": "Python for Beginners",
                "description": "Learn Python from scratch. Covers variables, loops, functions, OOP and more. Perfect for absolute beginners with zero coding experience.",
                "category": "Programming",
                "difficulty_level": "beginner",
                "lessons": [
                    {
                        "title": "Introduction to Python",
                        "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, Python is used in web development, data science, AI, automation, and more. In this lesson you will install Python, set up VS Code, and write your first Hello World program.",
                        "video_url": "https://www.youtube.com/embed/kqtD5dpn9C8",
                        "duration_minutes": 20,
                        "resources": [
                            {"title": "Python Introduction - GFG", "url": "https://www.geeksforgeeks.org/python-programming-language/", "type": "article"},
                            {"title": "Python Official Docs", "url": "https://docs.python.org/3/tutorial/", "type": "docs"},
                            {"title": "W3Schools Python", "url": "https://www.w3schools.com/python/", "type": "article"}
                        ]
                    },
                    {
                        "title": "Variables and Data Types",
                        "content": "Variables are containers for storing data values. Python has no command for declaring a variable — it is created the moment you assign a value. Python supports integers, floats, strings, booleans, lists, tuples, sets, and dictionaries. Understanding data types is fundamental to programming.",
                        "video_url": "https://www.youtube.com/embed/Z1Yd7upQsXY",
                        "duration_minutes": 30,
                        "resources": [
                            {"title": "Python Variables - GFG", "url": "https://www.geeksforgeeks.org/python-variables/", "type": "article"},
                            {"title": "Data Types in Python", "url": "https://www.geeksforgeeks.org/python-data-types/", "type": "article"},
                            {"title": "W3Schools Variables", "url": "https://www.w3schools.com/python/python_variables.asp", "type": "article"}
                        ]
                    },
                    {
                        "title": "Loops and Functions",
                        "content": "Loops allow you to execute a block of code repeatedly. Python has for loops and while loops. Functions are reusable blocks of code defined using the def keyword. They accept parameters and return values. Mastering loops and functions is essential for writing clean, efficient Python code.",
                        "video_url": "https://www.youtube.com/embed/94UHCEmprCY",
                        "duration_minutes": 35,
                        "resources": [
                            {"title": "Python Loops - GFG", "url": "https://www.geeksforgeeks.org/loops-in-python/", "type": "article"},
                            {"title": "Python Functions - GFG", "url": "https://www.geeksforgeeks.org/python-functions/", "type": "article"},
                            {"title": "W3Schools Loops", "url": "https://www.w3schools.com/python/python_for_loops.asp", "type": "article"}
                        ]
                    }
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
                "description": "Introduction to ML concepts including supervised learning, unsupervised learning, model evaluation and hands-on Scikit-learn projects.",
                "category": "Data Science",
                "difficulty_level": "intermediate",
                "lessons": [
                    {
                        "title": "What is Machine Learning?",
                        "content": "Machine Learning is a subset of Artificial Intelligence that enables systems to automatically learn and improve from experience without being explicitly programmed. There are three main types: Supervised Learning (learns from labeled data), Unsupervised Learning (finds patterns in unlabeled data), and Reinforcement Learning (learns through rewards and penalties).",
                        "video_url": "https://www.youtube.com/embed/ukzFI9rgwfU",
                        "duration_minutes": 25,
                        "resources": [
                            {"title": "Intro to ML - GFG", "url": "https://www.geeksforgeeks.org/machine-learning/", "type": "article"},
                            {"title": "ML Tutorial - W3Schools", "url": "https://www.w3schools.com/python/python_ml_getting_started.asp", "type": "article"},
                            {"title": "Scikit-learn Docs", "url": "https://scikit-learn.org/stable/getting_started.html", "type": "docs"}
                        ]
                    },
                    {
                        "title": "Supervised Learning Algorithms",
                        "content": "Supervised learning uses labeled training data to learn a mapping from inputs to outputs. Key algorithms include Linear Regression (predicts continuous values), Logistic Regression (binary classification), Decision Trees (tree-based rules), Random Forest (ensemble of trees), and Support Vector Machines (finds optimal boundary). Each has strengths for different problem types.",
                        "video_url": "https://www.youtube.com/embed/1vkb7BCMQd0",
                        "duration_minutes": 45,
                        "resources": [
                            {"title": "Supervised Learning - GFG", "url": "https://www.geeksforgeeks.org/supervised-unsupervised-learning/", "type": "article"},
                            {"title": "Random Forest - GFG", "url": "https://www.geeksforgeeks.org/random-forest-classifier-using-scikit-learn/", "type": "article"},
                            {"title": "Decision Trees - GFG", "url": "https://www.geeksforgeeks.org/decision-tree/", "type": "article"}
                        ]
                    },
                    {
                        "title": "Model Evaluation and Tuning",
                        "content": "Model evaluation tells you how well your ML model performs on unseen data. Key metrics include Accuracy, Precision, Recall, F1-Score, and ROC-AUC. The confusion matrix visualizes true/false positives and negatives. Cross-validation gives a more reliable estimate. Hyperparameter tuning with GridSearchCV or RandomizedSearchCV improves model performance.",
                        "video_url": "https://www.youtube.com/embed/85dtiMz9tSo",
                        "duration_minutes": 40,
                        "resources": [
                            {"title": "Model Evaluation - GFG", "url": "https://www.geeksforgeeks.org/metrics-for-machine-learning-model/", "type": "article"},
                            {"title": "Cross Validation - GFG", "url": "https://www.geeksforgeeks.org/cross-validation-machine-learning/", "type": "article"},
                            {"title": "Scikit-learn Metrics", "url": "https://scikit-learn.org/stable/modules/model_evaluation.html", "type": "docs"}
                        ]
                    }
                ],
                "quizzes": [
                    {
                        "title": "ML Concepts Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is supervised learning?", "a": "Learning without labels", "b": "Learning with labeled data", "c": "Learning by rewards", "d": "Finding clusters", "ans": "b"},
                            {"q": "Which is used for classification?", "a": "Linear Regression", "b": "K-Means", "c": "Random Forest", "d": "PCA", "ans": "c"},
                            {"q": "What does overfitting mean?", "a": "Model too simple", "b": "Performs well everywhere", "c": "Memorizes training data", "d": "Low accuracy", "ans": "c"},
                            {"q": "Purpose of train-test split?", "a": "Speed up training", "b": "Evaluate on unseen data", "c": "Reduce dataset", "d": "Clean data", "ans": "b"},
                            {"q": "Which metric measures classification?", "a": "MSE", "b": "RMSE", "c": "F1-Score", "d": "R-squared", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Web Development with React",
                "description": "Build modern web applications using React.js. Learn components, state management, hooks, routing, and connect to REST APIs.",
                "category": "Web Development",
                "difficulty_level": "intermediate",
                "lessons": [
                    {
                        "title": "React Fundamentals",
                        "content": "React is a JavaScript library for building user interfaces, developed by Facebook. It uses a component-based architecture where UIs are built from small, reusable pieces. JSX is a syntax extension that lets you write HTML inside JavaScript. The Virtual DOM makes React fast by minimizing direct DOM manipulation.",
                        "video_url": "https://www.youtube.com/embed/SqcY0GlETPk",
                        "duration_minutes": 30,
                        "resources": [
                            {"title": "React Tutorial - GFG", "url": "https://www.geeksforgeeks.org/reactjs/", "type": "article"},
                            {"title": "React Official Docs", "url": "https://react.dev/learn", "type": "docs"},
                            {"title": "W3Schools React", "url": "https://www.w3schools.com/react/", "type": "article"}
                        ]
                    },
                    {
                        "title": "State and Hooks",
                        "content": "React Hooks are functions that let you use state and lifecycle features in functional components. useState manages local state. useEffect handles side effects like API calls and subscriptions. useContext shares data globally without prop drilling. Custom hooks let you extract reusable stateful logic.",
                        "video_url": "https://www.youtube.com/embed/O6P86uwfdR0",
                        "duration_minutes": 40,
                        "resources": [
                            {"title": "React Hooks - GFG", "url": "https://www.geeksforgeeks.org/reactjs-hooks/", "type": "article"},
                            {"title": "useState Hook", "url": "https://react.dev/reference/react/useState", "type": "docs"},
                            {"title": "useEffect Hook", "url": "https://react.dev/reference/react/useEffect", "type": "docs"}
                        ]
                    },
                    {
                        "title": "React Router and APIs",
                        "content": "React Router v6 enables client-side routing without full page reloads. Define routes with Route components and navigate between pages. Axios is the most popular HTTP client for making API requests. Handle loading states, errors, and display dynamic data fetched from your FastAPI backend.",
                        "video_url": "https://www.youtube.com/embed/Ul3y1LXxzdU",
                        "duration_minutes": 35,
                        "resources": [
                            {"title": "React Router - GFG", "url": "https://www.geeksforgeeks.org/reactjs-router/", "type": "article"},
                            {"title": "Axios Tutorial - GFG", "url": "https://www.geeksforgeeks.org/axios-in-react/", "type": "article"},
                            {"title": "React Router Docs", "url": "https://reactrouter.com/en/main", "type": "docs"}
                        ]
                    }
                ],
                "quizzes": [
                    {
                        "title": "React Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is JSX?", "a": "Database language", "b": "JavaScript XML syntax", "c": "CSS framework", "d": "Testing library", "ans": "b"},
                            {"q": "Which hook manages state?", "a": "useEffect", "b": "useContext", "c": "useState", "d": "useRef", "ans": "c"},
                            {"q": "What are React props?", "a": "Internal state", "b": "DB connections", "c": "Read-only inputs", "d": "CSS properties", "ans": "c"},
                            {"q": "useEffect is used for?", "a": "Managing state", "b": "Side effects", "c": "Creating components", "d": "Styling", "ans": "b"},
                            {"q": "Virtual DOM purpose?", "a": "Store data", "b": "Render directly", "c": "Minimize DOM updates", "d": "Connect server", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Data Analysis with Pandas",
                "description": "Master data manipulation and analysis using Python Pandas. Clean, transform, and visualize real datasets.",
                "category": "Data Science",
                "difficulty_level": "beginner",
                "lessons": [
                    {
                        "title": "Introduction to Pandas",
                        "content": "Pandas is the most popular Python library for data manipulation and analysis. The two main data structures are Series (1D labeled array) and DataFrame (2D labeled table). Key operations include reading files with read_csv(), exploring data with head(), tail(), info(), describe(), and shape.",
                        "video_url": "https://www.youtube.com/embed/vmEHCJofslg",
                        "duration_minutes": 25,
                        "resources": [
                            {"title": "Pandas Tutorial - GFG", "url": "https://www.geeksforgeeks.org/pandas-tutorial/", "type": "article"},
                            {"title": "Pandas Official Docs", "url": "https://pandas.pydata.org/docs/getting_started/", "type": "docs"},
                            {"title": "W3Schools Pandas", "url": "https://www.w3schools.com/python/pandas/default.asp", "type": "article"}
                        ]
                    },
                    {
                        "title": "Data Cleaning",
                        "content": "Real-world data is messy. Data cleaning involves handling missing values with fillna() or dropna(), removing duplicate rows with drop_duplicates(), fixing incorrect data types with astype(), renaming columns with rename(), and filtering outliers. Clean data is essential for accurate analysis and ML models.",
                        "video_url": "https://www.youtube.com/embed/bDhvCp3_lYw",
                        "duration_minutes": 35,
                        "resources": [
                            {"title": "Data Cleaning - GFG", "url": "https://www.geeksforgeeks.org/data-cleaning-in-python/", "type": "article"},
                            {"title": "Handling Missing Data", "url": "https://www.geeksforgeeks.org/working-with-missing-data-in-pandas/", "type": "article"},
                            {"title": "Pandas Cleaning - W3Schools", "url": "https://www.w3schools.com/python/pandas/pandas_cleaning.asp", "type": "article"}
                        ]
                    },
                    {
                        "title": "Data Visualization",
                        "content": "Visualization helps discover patterns and communicate insights. Pandas integrates with Matplotlib and Seaborn. Use line plots for trends, bar charts for comparisons, histograms for distributions, scatter plots for relationships, and heatmaps for correlations. Good visualizations tell a story with your data.",
                        "video_url": "https://www.youtube.com/embed/r75BPh1uk38",
                        "duration_minutes": 30,
                        "resources": [
                            {"title": "Data Visualization - GFG", "url": "https://www.geeksforgeeks.org/data-visualization-using-python/", "type": "article"},
                            {"title": "Matplotlib Tutorial", "url": "https://www.geeksforgeeks.org/matplotlib-tutorial/", "type": "article"},
                            {"title": "Seaborn Tutorial", "url": "https://www.geeksforgeeks.org/seaborn-tutorial/", "type": "article"}
                        ]
                    }
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
                            {"q": "df.shape returns?", "a": "Column names", "b": "Data types", "c": "Rows and columns", "d": "Statistics", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Database Design with SQL",
                "description": "Learn relational database design, SQL queries, joins, and PostgreSQL from scratch.",
                "category": "Database",
                "difficulty_level": "beginner",
                "lessons": [
                    {
                        "title": "Introduction to SQL",
                        "content": "SQL (Structured Query Language) is the standard language for managing relational databases. Core commands include CREATE TABLE (defines structure), INSERT (adds data), SELECT (retrieves data), UPDATE (modifies data), and DELETE (removes data). SQL is used by virtually every application that stores persistent data.",
                        "video_url": "https://www.youtube.com/embed/HXV3zeQKqGY",
                        "duration_minutes": 30,
                        "resources": [
                            {"title": "SQL Tutorial - GFG", "url": "https://www.geeksforgeeks.org/sql-tutorial/", "type": "article"},
                            {"title": "W3Schools SQL", "url": "https://www.w3schools.com/sql/", "type": "article"},
                            {"title": "PostgreSQL Docs", "url": "https://www.postgresql.org/docs/current/tutorial.html", "type": "docs"}
                        ]
                    },
                    {
                        "title": "Joins and Relationships",
                        "content": "Relational databases store related data in separate tables linked by keys. INNER JOIN returns rows with matches in both tables. LEFT JOIN returns all rows from the left table. RIGHT JOIN returns all from the right. Foreign keys enforce referential integrity. Proper relationships eliminate data redundancy and ensure consistency.",
                        "video_url": "https://www.youtube.com/embed/9yeOJ0ZMUYw",
                        "duration_minutes": 35,
                        "resources": [
                            {"title": "SQL Joins - GFG", "url": "https://www.geeksforgeeks.org/sql-join-set-1-inner-left-right-and-full-joins/", "type": "article"},
                            {"title": "Foreign Keys - GFG", "url": "https://www.geeksforgeeks.org/foreign-key-constraint-in-sql/", "type": "article"},
                            {"title": "W3Schools Joins", "url": "https://www.w3schools.com/sql/sql_join.asp", "type": "article"}
                        ]
                    },
                    {
                        "title": "Advanced SQL",
                        "content": "Advanced SQL includes GROUP BY (aggregate by category), HAVING (filter after grouping), subqueries (nested SELECT), CTEs (WITH clause for readable queries), window functions (ROW_NUMBER, RANK, LAG), and indexes (speed up retrieval). Understanding ACID properties (Atomicity, Consistency, Isolation, Durability) is crucial for reliable transactions.",
                        "video_url": "https://www.youtube.com/embed/M-55BmjOuXY",
                        "duration_minutes": 40,
                        "resources": [
                            {"title": "Advanced SQL - GFG", "url": "https://www.geeksforgeeks.org/advanced-sql/", "type": "article"},
                            {"title": "SQL Indexes - GFG", "url": "https://www.geeksforgeeks.org/sql-indexes/", "type": "article"},
                            {"title": "Window Functions - GFG", "url": "https://www.geeksforgeeks.org/window-functions-in-sql/", "type": "article"}
                        ]
                    }
                ],
                "quizzes": [
                    {
                        "title": "SQL Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "Which command retrieves data?", "a": "INSERT", "b": "UPDATE", "c": "SELECT", "d": "DELETE", "ans": "c"},
                            {"q": "PRIMARY KEY does?", "a": "Encrypts data", "b": "Uniquely identifies rows", "c": "Links tables", "d": "Sorts data", "ans": "b"},
                            {"q": "INNER JOIN returns?", "a": "All left rows", "b": "All right rows", "c": "Matching rows from both", "d": "All rows", "ans": "c"},
                            {"q": "GROUP BY does?", "a": "Sort results", "b": "Filter rows", "c": "Group by column", "d": "Join tables", "ans": "c"},
                            {"q": "FOREIGN KEY is?", "a": "Unique identifier", "b": "Key from another table", "c": "Encrypted field", "d": "An index", "ans": "b"},
                        ]
                    }
                ]
            },
            {
                "title": "Statistics for Data Science",
                "description": "Build a strong foundation in statistics — probability, distributions, hypothesis testing essential for data science.",
                "category": "Data Science",
                "difficulty_level": "beginner",
                "lessons": [
                    {
                        "title": "Descriptive Statistics",
                        "content": "Descriptive statistics summarize and describe the features of a dataset. Measures of central tendency include mean (average), median (middle value), and mode (most frequent). Measures of spread include variance (average squared deviation), standard deviation (square root of variance), and range. These help you understand your data before modeling.",
                        "video_url": "https://www.youtube.com/embed/SzZ6GpcfoQY",
                        "duration_minutes": 25,
                        "resources": [
                            {"title": "Statistics Basics - GFG", "url": "https://www.geeksforgeeks.org/statistics-for-data-science/", "type": "article"},
                            {"title": "Mean Median Mode - GFG", "url": "https://www.geeksforgeeks.org/measures-of-central-tendency/", "type": "article"},
                            {"title": "W3Schools Statistics", "url": "https://www.w3schools.com/statistics/", "type": "article"}
                        ]
                    },
                    {
                        "title": "Probability and Distributions",
                        "content": "Probability measures the likelihood of an event occurring (0 to 1). Key distributions include Normal (bell curve, most common in nature), Binomial (success/failure trials), and Poisson (count of events in time). Bayes Theorem updates probability when new evidence arrives: P(A|B) = P(B|A) × P(A) / P(B). Used heavily in ML.",
                        "video_url": "https://www.youtube.com/embed/uzkc-qNVoOk",
                        "duration_minutes": 35,
                        "resources": [
                            {"title": "Probability - GFG", "url": "https://www.geeksforgeeks.org/probability/", "type": "article"},
                            {"title": "Normal Distribution - GFG", "url": "https://www.geeksforgeeks.org/normal-distribution/", "type": "article"},
                            {"title": "Bayes Theorem - GFG", "url": "https://www.geeksforgeeks.org/bayes-theorem/", "type": "article"}
                        ]
                    },
                    {
                        "title": "Hypothesis Testing",
                        "content": "Hypothesis testing uses statistics to determine if there is enough evidence to reject a null hypothesis. The p-value represents the probability of observing results by chance — if p < 0.05, reject the null hypothesis. Key tests include t-test (compare means), chi-square (categorical variables), and ANOVA (compare multiple groups).",
                        "video_url": "https://www.youtube.com/embed/0zZYBALbZgg",
                        "duration_minutes": 40,
                        "resources": [
                            {"title": "Hypothesis Testing - GFG", "url": "https://www.geeksforgeeks.org/hypothesis-testing/", "type": "article"},
                            {"title": "T-test - GFG", "url": "https://www.geeksforgeeks.org/t-test/", "type": "article"},
                            {"title": "p-value Explained - GFG", "url": "https://www.geeksforgeeks.org/p-value-in-statistics/", "type": "article"}
                        ]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Statistics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "Mean of [2,4,6,8]?", "a": "4", "b": "5", "c": "6", "d": "3", "ans": "b"},
                            {"q": "Standard deviation measures?", "a": "Central value", "b": "Spread around mean", "c": "Highest value", "d": "Sum", "ans": "b"},
                            {"q": "Normal distribution shape?", "a": "Skewed", "b": "Bell curve", "c": "Flat", "d": "U-shaped", "ans": "b"},
                            {"q": "p-value < 0.05 means?", "a": "Accept null hypothesis", "b": "Reject null hypothesis", "c": "Inconclusive", "d": "No relationship", "ans": "b"},
                            {"q": "Median of [1,3,5,7,9]?", "a": "3", "b": "7", "c": "5", "d": "4", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Deep Learning with TensorFlow",
                "description": "Build neural networks using TensorFlow and Keras for real-world AI applications.",
                "category": "AI",
                "difficulty_level": "advanced",
                "is_premium": True,      # ← ADDED
                "price": 999.00,         # ← ADDED
                "lessons": [
                    {
                        "title": "Neural Networks Basics",
                        "content": "A neural network is a series of layers of interconnected artificial neurons inspired by the human brain. Each neuron receives inputs, applies weights and a bias, then passes through an activation function (ReLU, Sigmoid, Softmax). Forward propagation computes predictions. Backpropagation computes gradients. Gradient descent updates weights to minimize loss.",
                        "video_url": "https://www.youtube.com/embed/aircAruvnKk",
                        "duration_minutes": 45,
                        "resources": [
                            {"title": "Neural Networks - GFG", "url": "https://www.geeksforgeeks.org/neural-networks-a-beginners-guide/", "type": "article"},
                            {"title": "Backpropagation - GFG", "url": "https://www.geeksforgeeks.org/backpropagation-in-neural-network/", "type": "article"},
                            {"title": "TensorFlow Docs", "url": "https://www.tensorflow.org/tutorials", "type": "docs"}
                        ]
                    },
                    {
                        "title": "Convolutional Neural Networks",
                        "content": "CNNs are specialized for processing grid-like data such as images. Convolutional layers apply filters to detect features like edges and shapes. Pooling layers reduce spatial dimensions. Flatten converts 2D feature maps to 1D. Dense layers make final predictions. CNNs power image recognition, face detection, and medical imaging AI.",
                        "video_url": "https://www.youtube.com/embed/YRhxdVk_sIs",
                        "duration_minutes": 50,
                        "resources": [
                            {"title": "CNN - GFG", "url": "https://www.geeksforgeeks.org/convolutional-neural-network-cnn-in-machine-learning/", "type": "article"},
                            {"title": "Image Classification - GFG", "url": "https://www.geeksforgeeks.org/image-classifier-using-cnn/", "type": "article"},
                            {"title": "Keras CNN Tutorial", "url": "https://keras.io/examples/vision/mnist_convnet/", "type": "docs"}
                        ]
                    },
                    {
                        "title": "Model Training and Deployment",
                        "content": "Training a deep learning model involves choosing a loss function (CrossEntropy for classification, MSE for regression) and an optimizer (Adam is most popular). Callbacks like EarlyStopping prevent overfitting by stopping training when validation loss stops improving. Save models with model.save(). Deploy using FastAPI, Flask, or TensorFlow Serving.",
                        "video_url": "https://www.youtube.com/embed/tpCFfeUEGs8",
                        "duration_minutes": 40,
                        "resources": [
                            {"title": "Model Training - GFG", "url": "https://www.geeksforgeeks.org/tensorflow-2-0-training-loop/", "type": "article"},
                            {"title": "Save and Load Models", "url": "https://www.tensorflow.org/tutorials/keras/save_and_load", "type": "docs"},
                            {"title": "Deploy ML Model - GFG", "url": "https://www.geeksforgeeks.org/deploy-machine-learning-model-using-flask/", "type": "article"}
                        ]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Deep Learning Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "What is a neural network?", "a": "A database", "b": "Interconnected artificial neurons", "c": "A sorting algorithm", "d": "A web framework", "ans": "b"},
                            {"q": "Sigmoid outputs?", "a": "Any number", "b": "0 to 1", "c": "-1 to 1", "d": "0 or 1 only", "ans": "b"},
                            {"q": "Backpropagation does?", "a": "Forward pass", "b": "Updates weights", "c": "Creates layers", "d": "Normalizes data", "ans": "b"},
                            {"q": "CNN is best for?", "a": "Text data", "b": "Time series", "c": "Image data", "d": "Tabular data", "ans": "c"},
                            {"q": "Dropout layer prevents?", "a": "Slow training", "b": "Missing neurons", "c": "Overfitting", "d": "Data loss", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "Natural Language Processing",
                "description": "Text preprocessing, sentiment analysis, and transformers using SpaCy and HuggingFace Transformers.",
                "category": "AI",
                "difficulty_level": "advanced",
                "is_premium": True,      # ← ADDED
                "price": 1299.00,        # ← ADDED
                "lessons": [
                    {
                        "title": "Text Preprocessing",
                        "content": "Raw text must be cleaned before feeding into ML models. Tokenization splits text into words or sentences. Stop word removal eliminates common words like 'the', 'is'. Stemming reduces words to root forms (running → run). Lemmatization returns dictionary forms. TF-IDF (Term Frequency-Inverse Document Frequency) converts text to numerical vectors representing word importance.",
                        "video_url": "https://www.youtube.com/embed/X2vAabgKiuM",
                        "duration_minutes": 35,
                        "resources": [
                            {"title": "NLP - GFG", "url": "https://www.geeksforgeeks.org/natural-language-processing-overview/", "type": "article"},
                            {"title": "Text Preprocessing - GFG", "url": "https://www.geeksforgeeks.org/text-preprocessing-in-python/", "type": "article"},
                            {"title": "NLTK Tutorial - GFG", "url": "https://www.geeksforgeeks.org/nltk-library-in-python/", "type": "article"}
                        ]
                    },
                    {
                        "title": "Sentiment Analysis",
                        "content": "Sentiment analysis classifies text as positive, negative, or neutral. Traditional approach uses Naive Bayes or Logistic Regression with TF-IDF features. Deep learning approach uses LSTM (Long Short-Term Memory) networks that understand word sequences. Pre-trained models like VADER work well for social media text without training.",
                        "video_url": "https://www.youtube.com/embed/i4D5DZ5ZG-0",
                        "duration_minutes": 40,
                        "resources": [
                            {"title": "Sentiment Analysis - GFG", "url": "https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/", "type": "article"},
                            {"title": "LSTM for NLP - GFG", "url": "https://www.geeksforgeeks.org/long-short-term-memory-networks-explanation/", "type": "article"},
                            {"title": "HuggingFace Sentiment", "url": "https://huggingface.co/docs/transformers/sentiment_analysis", "type": "docs"}
                        ]
                    },
                    {
                        "title": "Transformers and BERT",
                        "content": "Transformers revolutionized NLP in 2017. The attention mechanism allows the model to focus on relevant parts of the input regardless of position. BERT (Bidirectional Encoder Representations from Transformers) reads text in both directions simultaneously, giving deeper context understanding. Fine-tuning BERT on your dataset achieves state-of-the-art results.",
                        "video_url": "https://www.youtube.com/embed/4Bdc55j80l4",
                        "duration_minutes": 50,
                        "resources": [
                            {"title": "Transformers - GFG", "url": "https://www.geeksforgeeks.org/transformer-neural-network/", "type": "article"},
                            {"title": "BERT Explained - GFG", "url": "https://www.geeksforgeeks.org/explanation-of-bert-model-nlp/", "type": "article"},
                            {"title": "HuggingFace Transformers", "url": "https://huggingface.co/docs/transformers/quicktour", "type": "docs"}
                        ]
                    }
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
                            {"q": "BERT reads text?", "a": "Left to right only", "b": "Right to left only", "c": "Both directions", "d": "Random order", "ans": "c"},
                        ]
                    }
                ]
            },
            {
                "title": "DevOps and Docker",
                "description": "Containerization, CI/CD pipelines, Docker, and cloud deployment for modern software teams.",
                "category": "DevOps",
                "difficulty_level": "intermediate",
                "is_premium": True,      # ← ADDED
                "price": 799.00,         # ← ADDED
                "lessons": [
                    {
                        "title": "Introduction to Docker",
                        "content": "Docker is a platform that uses containerization to package applications with all their dependencies. Unlike virtual machines, containers share the host OS kernel making them lightweight and fast. A Docker image is a read-only template. A container is a running instance. Volumes persist data. Networks connect containers. The Dockerfile defines how to build an image.",
                        "video_url": "https://www.youtube.com/embed/3c-iBn73dDE",
                        "duration_minutes": 35,
                        "resources": [
                            {"title": "Docker Tutorial - GFG", "url": "https://www.geeksforgeeks.org/docker-tutorial/", "type": "article"},
                            {"title": "Docker Official Docs", "url": "https://docs.docker.com/get-started/", "type": "docs"},
                            {"title": "W3Schools Docker", "url": "https://www.w3schools.com/docker/", "type": "article"}
                        ]
                    },
                    {
                        "title": "Docker Compose",
                        "content": "Docker Compose orchestrates multi-container applications using a YAML file. Define all your services (web app, database, cache) in docker-compose.yml with their images, ports, volumes, and environment variables. One command `docker-compose up` starts everything. `docker-compose down` stops and removes containers. Perfect for development environments.",
                        "video_url": "https://www.youtube.com/embed/HG6yIjqMVjE",
                        "duration_minutes": 30,
                        "resources": [
                            {"title": "Docker Compose - GFG", "url": "https://www.geeksforgeeks.org/docker-compose/", "type": "article"},
                            {"title": "Compose File Reference", "url": "https://docs.docker.com/compose/compose-file/", "type": "docs"},
                            {"title": "Docker Compose Tutorial", "url": "https://www.geeksforgeeks.org/docker-compose-tutorial/", "type": "article"}
                        ]
                    },
                    {
                        "title": "CI/CD Pipelines",
                        "content": "CI/CD automates testing and deployment. Continuous Integration means every code push triggers automated tests. Continuous Delivery means tested code is automatically deployed to staging or production. GitHub Actions uses YAML workflow files to define pipelines. On every push: run tests → build Docker image → deploy to cloud. This eliminates manual deployment errors.",
                        "video_url": "https://www.youtube.com/embed/R8_veQiYBjI",
                        "duration_minutes": 40,
                        "resources": [
                            {"title": "CI/CD - GFG", "url": "https://www.geeksforgeeks.org/ci-cd-pipeline/", "type": "article"},
                            {"title": "GitHub Actions Docs", "url": "https://docs.github.com/en/actions", "type": "docs"},
                            {"title": "GitHub Actions - GFG", "url": "https://www.geeksforgeeks.org/github-actions/", "type": "article"}
                        ]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Docker and DevOps Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "Docker container is?", "a": "Virtual machine", "b": "Lightweight isolated env", "c": "Cloud server", "d": "Database", "ans": "b"},
                            {"q": "Dockerfile contains?", "a": "DB config", "b": "Build instructions", "c": "Network config", "d": "Deploy script", "ans": "b"},
                            {"q": "docker-compose up does?", "a": "Stops containers", "b": "Builds and starts services", "c": "Removes containers", "d": "Lists images", "ans": "b"},
                            {"q": "CI stands for?", "a": "Container Integration", "b": "Continuous Integration", "c": "Cloud Infrastructure", "d": "Code Inspection", "ans": "b"},
                            {"q": "Kubernetes is used for?", "a": "DB management", "b": "Container orchestration", "c": "Version control", "d": "Monitoring", "ans": "b"},
                        ]
                    }
                ]
            },
            {
                "title": "Git and Version Control",
                "description": "Master Git branching, merging, pull requests, and professional GitHub workflows.",
                "category": "Tools",
                "difficulty_level": "beginner",
                "lessons": [
                    {
                        "title": "Git Basics",
                        "content": "Git is a distributed version control system that tracks changes in your code over time. Every developer has a full copy of the repository. The working directory is where you edit files. The staging area (index) holds changes ready to commit. The repository stores committed history. Key commands: git init, git clone, git add, git commit, git push, git pull.",
                        "video_url": "https://www.youtube.com/embed/RGOj5yH7evk",
                        "duration_minutes": 25,
                        "resources": [
                            {"title": "Git Tutorial - GFG", "url": "https://www.geeksforgeeks.org/git-tutorial/", "type": "article"},
                            {"title": "Git Official Docs", "url": "https://git-scm.com/doc", "type": "docs"},
                            {"title": "W3Schools Git", "url": "https://www.w3schools.com/git/", "type": "article"}
                        ]
                    },
                    {
                        "title": "Branching and Merging",
                        "content": "Branches allow parallel development without affecting the main codebase. Create a branch with git checkout -b feature-name. Switch branches with git checkout. Merge completed work with git merge. Conflicts occur when two branches change the same lines — resolve by editing the conflicting file and committing. Always create feature branches, never commit directly to main.",
                        "video_url": "https://www.youtube.com/embed/e2IbNHi4uCI",
                        "duration_minutes": 30,
                        "resources": [
                            {"title": "Git Branching - GFG", "url": "https://www.geeksforgeeks.org/git-branching/", "type": "article"},
                            {"title": "Merge vs Rebase - GFG", "url": "https://www.geeksforgeeks.org/git-merge-vs-rebase/", "type": "article"},
                            {"title": "Git Branch Docs", "url": "https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell", "type": "docs"}
                        ]
                    },
                    {
                        "title": "GitHub Workflows",
                        "content": "GitHub is the most popular hosting platform for Git repositories. Pull Requests let you propose changes and get code review before merging. Forks create personal copies of others repositories. Issues track bugs and features. GitHub Actions automates workflows. Professional teams use Git Flow (feature, develop, release, hotfix branches) or trunk-based development.",
                        "video_url": "https://www.youtube.com/embed/i_23KUAEtUM",
                        "duration_minutes": 35,
                        "resources": [
                            {"title": "GitHub Tutorial - GFG", "url": "https://www.geeksforgeeks.org/introduction-to-github/", "type": "article"},
                            {"title": "Pull Requests - GFG", "url": "https://www.geeksforgeeks.org/git-pull-request/", "type": "article"},
                            {"title": "GitHub Docs", "url": "https://docs.github.com/en/get-started", "type": "docs"}
                        ]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Git Basics Quiz",
                        "pass_marks": 3,
                        "questions": [
                            {"q": "git init does?", "a": "Clones repo", "b": "Initializes new repo", "c": "Pushes code", "d": "Creates branch", "ans": "b"},
                            {"q": "git add does?", "a": "Commits changes", "b": "Stages files", "c": "Pushes to remote", "d": "Creates branch", "ans": "b"},
                            {"q": "git push does?", "a": "Downloads code", "b": "Saves locally", "c": "Uploads to remote", "d": "Creates branch", "ans": "c"},
                            {"q": "What is a branch?", "a": "Full project copy", "b": "Independent dev line", "c": "Remote server", "d": "Commit history", "ans": "b"},
                            {"q": "Pull Request is?", "a": "Download request", "b": "Merge proposal", "c": "New branch", "d": "Delete request", "ans": "b"},
                        ]
                    }
                ]
            },
        ]

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
                is_published=True,
                is_premium=course_data.get("is_premium", False),  # ← UPDATED
                price=course_data.get("price", 0.00)              # ← UPDATED
            )
            db.add(course)
            db.commit()
            db.refresh(course)

            for i, ld in enumerate(course_data["lessons"]):
                db.add(Lesson(
                    course_id=course.id,
                    title=ld["title"],
                    content=ld["content"],
                    video_url=ld.get("video_url", ""),
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
        print(f"🎉 Seed complete! {total} courses with real content ready.")

    except Exception as e:
        print(f"❌ Seed error: {e}")
        db.rollback()
    finally:
        db.close()