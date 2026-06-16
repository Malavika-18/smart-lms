"""
Seed script — auto-populates Smart LMS with courses, quizzes and questions.
Run once after setting up the database:
    python seed_data.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.course import Course, Lesson
from app.models.quiz import Quiz, Question
from app.utils.auth import hash_password

# ──────────────────────────────────────────
# SEED DATA
# ──────────────────────────────────────────

USERS = [
    {
        "full_name": "Admin User",
        "email": "admin@smartlms.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Dr. Sarah Johnson",
        "email": "teacher@smartlms.com",
        "password": "teacher123",
        "role": "teacher"
    }
]

COURSES = [
    {
        "title": "Python for Beginners",
        "description": "Learn Python from scratch. Covers variables, loops, functions, OOP and more. Perfect for absolute beginners.",
        "category": "Programming",
        "difficulty_level": "beginner",
        "lessons": [
            {"title": "Introduction to Python", "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. In this lesson we cover installation, setting up VS Code, and writing your first Hello World program.", "duration_minutes": 20},
            {"title": "Variables and Data Types", "content": "Learn about integers, floats, strings, booleans, lists, tuples, and dictionaries. Understand how Python handles dynamic typing and how to convert between types.", "duration_minutes": 30},
            {"title": "Loops and Functions", "content": "Master for loops, while loops, break and continue statements. Then learn to define reusable functions with parameters, return values, and default arguments.", "duration_minutes": 35},
        ],
        "quizzes": [
            {
                "title": "Python Basics Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is the correct way to print in Python?", "a": "print('Hello')", "b": "echo('Hello')", "c": "printf('Hello')", "d": "console.log('Hello')", "ans": "a"},
                    {"q": "Which data type is used for decimal numbers?", "a": "int", "b": "str", "c": "float", "d": "bool", "ans": "c"},
                    {"q": "How do you start a for loop in Python?", "a": "for i in range(10):", "b": "for (i=0; i<10; i++)", "c": "loop i from 0 to 10", "d": "foreach i in 10", "ans": "a"},
                    {"q": "What does len() function do?", "a": "Returns length of an object", "b": "Converts to integer", "c": "Creates a list", "d": "Prints output", "ans": "a"},
                    {"q": "Which keyword defines a function in Python?", "a": "function", "b": "def", "c": "fun", "d": "define", "ans": "b"},
                ]
            },
            {
                "title": "Python Data Structures Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "How do you create an empty list in Python?", "a": "list = {}", "b": "list = []", "c": "list = ()", "d": "list = <>", "ans": "b"},
                    {"q": "Which method adds an item to a list?", "a": "list.add()", "b": "list.push()", "c": "list.append()", "d": "list.insert()", "ans": "c"},
                    {"q": "What is a dictionary in Python?", "a": "Ordered sequence", "b": "Key-value pairs", "c": "Set of unique items", "d": "Immutable list", "ans": "b"},
                    {"q": "How do you access dictionary value by key?", "a": "dict[key]", "b": "dict.get[key]", "c": "dict->key", "d": "dict::key", "ans": "a"},
                    {"q": "What does tuple mean in Python?", "a": "Mutable ordered list", "b": "Immutable ordered sequence", "c": "Unordered set", "d": "Key-value store", "ans": "b"},
                ]
            }
        ]
    },
    {
        "title": "Machine Learning Fundamentals",
        "description": "Introduction to ML concepts including supervised learning, unsupervised learning, model evaluation, and hands-on with Scikit-learn.",
        "category": "Data Science",
        "difficulty_level": "intermediate",
        "lessons": [
            {"title": "What is Machine Learning?", "content": "Machine Learning is a subset of AI that enables systems to learn from data. We cover the types: supervised, unsupervised, and reinforcement learning with real-world examples.", "duration_minutes": 25},
            {"title": "Supervised Learning Algorithms", "content": "Deep dive into Linear Regression, Logistic Regression, Decision Trees, Random Forest, and SVM. Learn when to use each algorithm and how to evaluate them.", "duration_minutes": 45},
            {"title": "Model Evaluation & Tuning", "content": "Learn accuracy, precision, recall, F1-score, confusion matrix. Understand overfitting vs underfitting. Master cross-validation and hyperparameter tuning.", "duration_minutes": 40},
        ],
        "quizzes": [
            {
                "title": "ML Concepts Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is supervised learning?", "a": "Learning without labels", "b": "Learning with labeled data", "c": "Learning by rewards", "d": "Learning from clusters", "ans": "b"},
                    {"q": "Which algorithm is used for classification?", "a": "Linear Regression", "b": "K-Means", "c": "Random Forest", "d": "PCA", "ans": "c"},
                    {"q": "What does overfitting mean?", "a": "Model is too simple", "b": "Model performs well on all data", "c": "Model memorizes training data", "d": "Model has low accuracy", "ans": "c"},
                    {"q": "What is the purpose of train-test split?", "a": "Speed up training", "b": "Evaluate on unseen data", "c": "Reduce dataset size", "d": "Clean the data", "ans": "b"},
                    {"q": "Which metric measures classification accuracy?", "a": "MSE", "b": "RMSE", "c": "F1-Score", "d": "R-squared", "ans": "c"},
                ]
            },
            {
                "title": "ML Algorithms Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What does KNN stand for?", "a": "K Nearest Neighbors", "b": "K Neural Networks", "c": "K Normalized Nodes", "d": "K Numeric Nodes", "ans": "a"},
                    {"q": "Random Forest is an ensemble of?", "a": "Neural Networks", "b": "Decision Trees", "c": "SVMs", "d": "KNN models", "ans": "b"},
                    {"q": "Which learning type uses reward/penalty?", "a": "Supervised", "b": "Unsupervised", "c": "Reinforcement", "d": "Semi-supervised", "ans": "c"},
                    {"q": "PCA is used for?", "a": "Classification", "b": "Clustering", "c": "Dimensionality Reduction", "d": "Regression", "ans": "c"},
                    {"q": "Which algorithm creates natural groupings?", "a": "Linear Regression", "b": "K-Means Clustering", "c": "Logistic Regression", "d": "Random Forest", "ans": "b"},
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
            {"title": "React Fundamentals", "content": "Understand JSX, components, props, and the Virtual DOM. Learn the difference between functional and class components and why hooks replaced class components.", "duration_minutes": 30},
            {"title": "State and Hooks", "content": "Master useState, useEffect, useContext, and custom hooks. Learn how state changes trigger re-renders and how to manage side effects properly.", "duration_minutes": 40},
            {"title": "React Router and APIs", "content": "Set up client-side routing with React Router v6. Learn to fetch data from REST APIs using Axios, handle loading states, and display dynamic content.", "duration_minutes": 35},
        ],
        "quizzes": [
            {
                "title": "React Basics Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is JSX in React?", "a": "A database query language", "b": "JavaScript XML syntax extension", "c": "A CSS framework", "d": "A testing library", "ans": "b"},
                    {"q": "Which hook manages component state?", "a": "useEffect", "b": "useContext", "c": "useState", "d": "useRef", "ans": "c"},
                    {"q": "What are React props?", "a": "Internal state variables", "b": "Database connections", "c": "Read-only inputs to components", "d": "CSS properties", "ans": "c"},
                    {"q": "useEffect is used for?", "a": "Managing state", "b": "Handling side effects", "c": "Creating components", "d": "Styling elements", "ans": "b"},
                    {"q": "What does the Virtual DOM do?", "a": "Stores data in memory", "b": "Renders HTML directly", "c": "Minimizes real DOM updates", "d": "Connects to a server", "ans": "c"},
                ]
            },
            {
                "title": "React Advanced Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "Which library handles routing in React?", "a": "axios", "b": "react-router-dom", "c": "redux", "d": "react-query", "ans": "b"},
                    {"q": "What is the purpose of useContext?", "a": "Fetch API data", "b": "Share state globally", "c": "Handle form input", "d": "Animate components", "ans": "b"},
                    {"q": "How do you pass data from parent to child?", "a": "Using state", "b": "Using refs", "c": "Using props", "d": "Using context", "ans": "c"},
                    {"q": "What triggers a component re-render?", "a": "CSS changes", "b": "State or prop changes", "c": "API calls", "d": "URL changes", "ans": "b"},
                    {"q": "Which tool builds React projects fast?", "a": "Webpack", "b": "Gulp", "c": "Vite", "d": "Grunt", "ans": "c"},
                ]
            }
        ]
    },
    {
        "title": "Data Analysis with Pandas",
        "description": "Master data manipulation and analysis using Python's Pandas library. Learn to clean, transform, visualize, and derive insights from real datasets.",
        "category": "Data Science",
        "difficulty_level": "beginner",
        "lessons": [
            {"title": "Introduction to Pandas", "content": "Learn what Pandas is and why it is essential for data science. Understand DataFrames and Series, how to create them, and basic operations like head(), tail(), info(), and describe().", "duration_minutes": 25},
            {"title": "Data Cleaning", "content": "Handle missing values with fillna() and dropna(). Remove duplicates, fix data types, rename columns, and filter rows. Learn how to deal with outliers and inconsistent data.", "duration_minutes": 35},
            {"title": "Data Visualization", "content": "Use Pandas built-in plotting along with Matplotlib and Seaborn to create line charts, bar graphs, histograms, scatter plots, and heatmaps to visualize your data insights.", "duration_minutes": 30},
        ],
        "quizzes": [
            {
                "title": "Pandas Basics Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is a Pandas DataFrame?", "a": "A Python list", "b": "A 2D labeled data structure", "c": "A neural network", "d": "A database", "ans": "b"},
                    {"q": "How do you read a CSV file in Pandas?", "a": "pd.open_csv()", "b": "pd.load()", "c": "pd.read_csv()", "d": "pd.import_csv()", "ans": "c"},
                    {"q": "Which method shows first 5 rows?", "a": "df.top()", "b": "df.first()", "c": "df.head()", "d": "df.start()", "ans": "c"},
                    {"q": "How do you drop missing values?", "a": "df.remove_na()", "b": "df.dropna()", "c": "df.clean()", "d": "df.delete_null()", "ans": "b"},
                    {"q": "What does df.shape return?", "a": "Column names", "b": "Data types", "c": "Rows and columns count", "d": "Summary statistics", "ans": "c"},
                ]
            },
            {
                "title": "Pandas Operations Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "How do you select a column in Pandas?", "a": "df->column", "b": "df.select(column)", "c": "df['column']", "d": "df::column", "ans": "c"},
                    {"q": "Which method groups data?", "a": "df.cluster()", "b": "df.groupby()", "c": "df.aggregate()", "d": "df.combine()", "ans": "b"},
                    {"q": "How do you sort a DataFrame?", "a": "df.order_by()", "b": "df.arrange()", "c": "df.sort_values()", "d": "df.rank()", "ans": "c"},
                    {"q": "What does df.describe() show?", "a": "Column names", "b": "Missing values", "c": "Statistical summary", "d": "Data types", "ans": "c"},
                    {"q": "How do you merge two DataFrames?", "a": "pd.combine()", "b": "pd.merge()", "c": "pd.join()", "d": "pd.concat()", "ans": "b"},
                ]
            }
        ]
    },
    {
        "title": "Deep Learning with TensorFlow",
        "description": "Build neural networks using TensorFlow and Keras. Cover perceptrons, CNNs, RNNs, and deploy real deep learning models.",
        "category": "Data Science",
        "difficulty_level": "advanced",
        "lessons": [
            {"title": "Neural Networks Basics", "content": "Understand artificial neurons, activation functions, forward propagation, backpropagation, and gradient descent. Build your first neural network with Keras Sequential API.", "duration_minutes": 45},
            {"title": "Convolutional Neural Networks", "content": "Learn CNNs for image recognition. Understand convolution layers, pooling, flatten, and dense layers. Build an image classifier on the MNIST dataset.", "duration_minutes": 50},
            {"title": "Model Training & Deployment", "content": "Train models with callbacks, early stopping, and learning rate schedules. Save and load models. Deploy using FastAPI and TensorFlow Serving.", "duration_minutes": 40},
        ],
        "quizzes": [
            {
                "title": "Deep Learning Basics Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is a neural network?", "a": "A database system", "b": "A set of interconnected artificial neurons", "c": "A sorting algorithm", "d": "A web framework", "ans": "b"},
                    {"q": "Which activation function outputs 0 or 1?", "a": "ReLU", "b": "Tanh", "c": "Sigmoid", "d": "Softmax", "ans": "c"},
                    {"q": "What does backpropagation do?", "a": "Forward pass data", "b": "Updates weights to reduce error", "c": "Creates neural layers", "d": "Normalizes data", "ans": "b"},
                    {"q": "CNN stands for?", "a": "Connected Neural Node", "b": "Convolutional Neural Network", "c": "Computed Numeric Network", "d": "Clustered Node Network", "ans": "b"},
                    {"q": "What is overfitting in deep learning?", "a": "High training and test accuracy", "b": "Low training accuracy", "c": "High training accuracy, low test accuracy", "d": "Equal train and test loss", "ans": "c"},
                ]
            },
            {
                "title": "TensorFlow & Keras Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "Which API builds models layer by layer?", "a": "TensorFlow Core", "b": "Keras Sequential", "c": "PyTorch Module", "d": "NumPy Stack", "ans": "b"},
                    {"q": "What is a dropout layer used for?", "a": "Speed up training", "b": "Add more neurons", "c": "Prevent overfitting", "d": "Normalize inputs", "ans": "c"},
                    {"q": "Which optimizer is most commonly used?", "a": "SGD only", "b": "Adam", "c": "RMSprop only", "d": "Adagrad", "ans": "b"},
                    {"q": "What does model.fit() do?", "a": "Evaluates the model", "b": "Saves the model", "c": "Trains the model", "d": "Loads weights", "ans": "c"},
                    {"q": "What is a loss function?", "a": "Measures model speed", "b": "Measures prediction error", "c": "Counts parameters", "d": "Splits data", "ans": "b"},
                ]
            }
        ]
    },
    {
        "title": "Database Design with SQL",
        "description": "Learn relational database design, SQL queries, joins, indexing, transactions, and PostgreSQL. Build real-world database schemas.",
        "category": "Database",
        "difficulty_level": "beginner",
        "lessons": [
            {"title": "Introduction to SQL", "content": "Understand relational databases, tables, rows, and columns. Learn CREATE, INSERT, SELECT, UPDATE, and DELETE statements with practical examples.", "duration_minutes": 30},
            {"title": "Joins and Relationships", "content": "Master INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN. Understand primary keys, foreign keys, and how to design normalized database schemas.", "duration_minutes": 35},
            {"title": "Advanced SQL", "content": "Learn GROUP BY, HAVING, subqueries, CTEs, window functions, and indexes. Understand transactions, ACID properties, and database optimization techniques.", "duration_minutes": 40},
        ],
        "quizzes": [
            {
                "title": "SQL Basics Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "Which SQL command retrieves data?", "a": "INSERT", "b": "UPDATE", "c": "SELECT", "d": "DELETE", "ans": "c"},
                    {"q": "What does PRIMARY KEY do?", "a": "Encrypts data", "b": "Uniquely identifies each row", "c": "Links two tables", "d": "Sorts data", "ans": "b"},
                    {"q": "Which JOIN returns all matching rows from both tables?", "a": "LEFT JOIN", "b": "RIGHT JOIN", "c": "INNER JOIN", "d": "OUTER JOIN", "ans": "c"},
                    {"q": "What does GROUP BY do?", "a": "Sorts results", "b": "Filters rows", "c": "Groups rows by column value", "d": "Joins tables", "ans": "c"},
                    {"q": "Which command removes all rows from a table?", "a": "DROP", "b": "DELETE", "c": "TRUNCATE", "d": "REMOVE", "ans": "c"},
                ]
            },
            {
                "title": "Advanced SQL Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is a FOREIGN KEY?", "a": "A unique identifier", "b": "A key from another table", "c": "An encrypted field", "d": "An index", "ans": "b"},
                    {"q": "What does HAVING clause do?", "a": "Filters before grouping", "b": "Filters after grouping", "c": "Sorts groups", "d": "Joins groups", "ans": "b"},
                    {"q": "What is normalization?", "a": "Speeding up queries", "b": "Removing data redundancy", "c": "Encrypting data", "d": "Indexing tables", "ans": "b"},
                    {"q": "What does an INDEX do?", "a": "Deletes duplicate rows", "b": "Speeds up data retrieval", "c": "Creates backups", "d": "Encrypts columns", "ans": "b"},
                    {"q": "What are ACID properties?", "a": "Database security rules", "b": "Transaction reliability guarantees", "c": "Query optimization rules", "d": "Data encryption standards", "ans": "b"},
                ]
            }
        ]
    },
    {
        "title": "Natural Language Processing",
        "description": "Explore NLP techniques including text preprocessing, sentiment analysis, named entity recognition, and building chatbots using SpaCy and Transformers.",
        "category": "AI",
        "difficulty_level": "advanced",
        "lessons": [
            {"title": "Text Preprocessing", "content": "Learn tokenization, stemming, lemmatization, stop word removal, and TF-IDF vectorization. Understand how to prepare raw text for machine learning models.", "duration_minutes": 35},
            {"title": "Sentiment Analysis", "content": "Build a sentiment classifier using Naive Bayes and LSTM. Understand positive, negative, and neutral classification. Work with real Twitter and product review datasets.", "duration_minutes": 40},
            {"title": "Transformers and BERT", "content": "Understand the attention mechanism and transformer architecture. Fine-tune BERT for text classification. Use HuggingFace Transformers library for state-of-the-art NLP.", "duration_minutes": 50},
        ],
        "quizzes": [
            {
                "title": "NLP Fundamentals Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is tokenization in NLP?", "a": "Encrypting text", "b": "Splitting text into words or sentences", "c": "Translating text", "d": "Summarizing text", "ans": "b"},
                    {"q": "What does TF-IDF measure?", "a": "Text length", "b": "Word frequency and importance", "c": "Sentence similarity", "d": "Grammar errors", "ans": "b"},
                    {"q": "What is stemming?", "a": "Adding prefixes to words", "b": "Reducing words to root form", "c": "Translating words", "d": "Counting words", "ans": "b"},
                    {"q": "What is sentiment analysis?", "a": "Summarizing text", "b": "Detecting emotion or opinion in text", "c": "Translating languages", "d": "Extracting keywords", "ans": "b"},
                    {"q": "BERT stands for?", "a": "Basic Encoding Representation Technique", "b": "Bidirectional Encoder Representations from Transformers", "c": "Binary Encoding for Text Recognition", "d": "Batch Encoded Response Tokens", "ans": "b"},
                ]
            },
            {
                "title": "NLP Models Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is a stop word?", "a": "Important keyword", "b": "Common word with little meaning", "c": "Verb in a sentence", "d": "Named entity", "ans": "b"},
                    {"q": "What is Named Entity Recognition?", "a": "Classifying text sentiment", "b": "Identifying names, places, dates in text", "c": "Translating text", "d": "Summarizing documents", "ans": "b"},
                    {"q": "What is the attention mechanism?", "a": "Focus on important parts of input", "b": "Speed up computation", "c": "Reduce model size", "d": "Encrypt text", "ans": "a"},
                    {"q": "Which library provides pre-trained NLP models?", "a": "Scikit-learn", "b": "Pandas", "c": "HuggingFace Transformers", "d": "Matplotlib", "ans": "c"},
                    {"q": "What is word embedding?", "a": "Counting word frequency", "b": "Converting words to numerical vectors", "c": "Removing punctuation", "d": "Splitting sentences", "ans": "b"},
                ]
            }
        ]
    },
    {
        "title": "DevOps and Docker",
        "description": "Learn containerization, CI/CD pipelines, Docker, Kubernetes basics, and cloud deployment. Essential skills for modern software development.",
        "category": "DevOps",
        "difficulty_level": "intermediate",
        "lessons": [
            {"title": "Introduction to Docker", "content": "Understand containers vs virtual machines. Learn Docker architecture, images, containers, volumes, and networks. Write Dockerfiles and build your first container.", "duration_minutes": 35},
            {"title": "Docker Compose", "content": "Orchestrate multi-container applications with Docker Compose. Define services, networks, and volumes in YAML. Run full-stack apps with a single command.", "duration_minutes": 30},
            {"title": "CI/CD Pipelines", "content": "Set up automated testing and deployment with GitHub Actions. Understand continuous integration, continuous delivery, and how to deploy automatically on every push.", "duration_minutes": 40},
        ],
        "quizzes": [
            {
                "title": "Docker Basics Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is a Docker container?", "a": "A virtual machine", "b": "A lightweight isolated environment", "c": "A cloud server", "d": "A database", "ans": "b"},
                    {"q": "What is a Dockerfile?", "a": "A configuration for databases", "b": "Instructions to build a Docker image", "c": "A network configuration file", "d": "A deployment script", "ans": "b"},
                    {"q": "Which command builds a Docker image?", "a": "docker run", "b": "docker pull", "c": "docker build", "d": "docker start", "ans": "c"},
                    {"q": "What does docker-compose up do?", "a": "Stops all containers", "b": "Builds and starts all services", "c": "Removes containers", "d": "Lists images", "ans": "b"},
                    {"q": "What is a Docker volume?", "a": "Network setting", "b": "CPU allocation", "c": "Persistent data storage", "d": "Memory limit", "ans": "c"},
                ]
            },
            {
                "title": "DevOps Concepts Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What does CI stand for in CI/CD?", "a": "Container Integration", "b": "Continuous Integration", "c": "Cloud Infrastructure", "d": "Code Inspection", "ans": "b"},
                    {"q": "What is Kubernetes used for?", "a": "Database management", "b": "Container orchestration", "c": "Code version control", "d": "Network monitoring", "ans": "b"},
                    {"q": "What is the purpose of a .dockerignore file?", "a": "List containers to stop", "b": "Exclude files from Docker build", "c": "Define environment variables", "d": "Configure networking", "ans": "b"},
                    {"q": "What does CD stand for in CI/CD?", "a": "Code Deployment", "b": "Container Delivery", "c": "Continuous Delivery", "d": "Cloud Development", "ans": "c"},
                    {"q": "What is a Docker registry?", "a": "List of running containers", "b": "Storage for Docker images", "c": "Network of containers", "d": "Container logs storage", "ans": "b"},
                ]
            }
        ]
    },
    {
        "title": "Statistics for Data Science",
        "description": "Build a strong foundation in statistics. Learn probability, distributions, hypothesis testing, correlation, and regression — essential for any data scientist.",
        "category": "Data Science",
        "difficulty_level": "beginner",
        "lessons": [
            {"title": "Descriptive Statistics", "content": "Understand mean, median, mode, variance, standard deviation, and percentiles. Learn how to summarize and describe datasets using these fundamental measures.", "duration_minutes": 25},
            {"title": "Probability and Distributions", "content": "Learn probability rules, Bayes theorem, normal distribution, binomial distribution, and Poisson distribution. Understand how random variables work in data science.", "duration_minutes": 35},
            {"title": "Hypothesis Testing", "content": "Understand null and alternative hypotheses, p-values, t-tests, chi-square tests, and ANOVA. Learn how to draw conclusions from data with statistical confidence.", "duration_minutes": 40},
        ],
        "quizzes": [
            {
                "title": "Statistics Basics Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is the mean of [2, 4, 6, 8]?", "a": "4", "b": "5", "c": "6", "d": "3", "ans": "b"},
                    {"q": "What does standard deviation measure?", "a": "Central value", "b": "Spread of data around mean", "c": "Highest value", "d": "Sum of values", "ans": "b"},
                    {"q": "What is a normal distribution also called?", "a": "Skewed curve", "b": "Bell curve", "c": "Flat distribution", "d": "Binomial curve", "ans": "b"},
                    {"q": "What does p-value represent?", "a": "Prediction accuracy", "b": "Probability of results by chance", "c": "Model performance", "d": "Data size", "ans": "b"},
                    {"q": "What is the median of [1, 3, 5, 7, 9]?", "a": "3", "b": "7", "c": "5", "d": "4", "ans": "c"},
                ]
            },
            {
                "title": "Probability Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is Bayes Theorem used for?", "a": "Sorting data", "b": "Updating probability with new evidence", "c": "Clustering data", "d": "Regression analysis", "ans": "b"},
                    {"q": "What is a random variable?", "a": "A fixed constant", "b": "A variable with random outcomes", "c": "An unknown parameter", "d": "A data column", "ans": "b"},
                    {"q": "What does correlation measure?", "a": "Causation between variables", "b": "Linear relationship strength", "c": "Data distribution", "d": "Model accuracy", "ans": "b"},
                    {"q": "What is a hypothesis test?", "a": "Testing code bugs", "b": "Statistical test to validate assumptions", "c": "Model training process", "d": "Data visualization", "ans": "b"},
                    {"q": "Variance is the square of?", "a": "Mean", "b": "Median", "c": "Standard Deviation", "d": "Range", "ans": "c"},
                ]
            }
        ]
    },
    {
        "title": "Git and Version Control",
        "description": "Master Git from basics to advanced. Learn branching, merging, pull requests, conflict resolution, and professional GitHub workflows used in real teams.",
        "category": "Tools",
        "difficulty_level": "beginner",
        "lessons": [
            {"title": "Git Basics", "content": "Install Git and configure your identity. Learn init, clone, add, commit, push, and pull. Understand the working directory, staging area, and repository.", "duration_minutes": 25},
            {"title": "Branching and Merging", "content": "Create and switch branches. Merge branches and resolve conflicts. Understand HEAD, detached HEAD, and how Git tracks changes through commits.", "duration_minutes": 30},
            {"title": "GitHub Workflows", "content": "Learn pull requests, code reviews, fork workflow, and GitHub Actions. Understand professional team workflows including Git Flow and trunk-based development.", "duration_minutes": 35},
        ],
        "quizzes": [
            {
                "title": "Git Basics Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "Which command initializes a Git repo?", "a": "git start", "b": "git create", "c": "git init", "d": "git new", "ans": "c"},
                    {"q": "Which command stages files for commit?", "a": "git commit", "b": "git add", "c": "git push", "d": "git stage", "ans": "b"},
                    {"q": "What does git push do?", "a": "Downloads code", "b": "Saves locally", "c": "Uploads to remote repository", "d": "Creates a branch", "ans": "c"},
                    {"q": "What is a Git branch?", "a": "A copy of the entire project", "b": "An independent line of development", "c": "A remote server", "d": "A commit history", "ans": "b"},
                    {"q": "What does git merge do?", "a": "Deletes a branch", "b": "Combines two branches", "c": "Creates a new repo", "d": "Reverts changes", "ans": "b"},
                ]
            },
            {
                "title": "GitHub Workflow Quiz",
                "pass_marks": 3,
                "questions": [
                    {"q": "What is a Pull Request?", "a": "Downloading code", "b": "Request to merge code into main branch", "c": "Creating a new branch", "d": "Deleting old commits", "ans": "b"},
                    {"q": "What does git clone do?", "a": "Creates a new branch", "b": "Copies a remote repo locally", "c": "Merges branches", "d": "Pushes changes", "ans": "b"},
                    {"q": "What is a merge conflict?", "a": "Failed push", "b": "Two branches changed same code", "c": "Missing commit", "d": "Wrong branch name", "ans": "b"},
                    {"q": "What does git stash do?", "a": "Deletes changes", "b": "Temporarily saves uncommitted changes", "c": "Creates a tag", "d": "Merges branches", "ans": "b"},
                    {"q": "What is the main/master branch?", "a": "A testing branch", "b": "The primary production branch", "c": "A developer branch", "d": "A backup branch", "ans": "b"},
                ]
            }
        ]
    },
]


# ──────────────────────────────────────────
# SEED FUNCTION
# ──────────────────────────────────────────

def seed():
    db = SessionLocal()
    print("\n🌱 Starting Smart LMS Seed Script...")
    print("=" * 50)

    try:
        # ── Create Users ──
        print("\n👤 Creating users...")
        teacher = None
        for u in USERS:
            exists = db.query(User).filter(User.email == u["email"]).first()
            if exists:
                print(f"   ⚠️  User already exists: {u['email']}")
                if u["role"] == "teacher":
                    teacher = exists
                continue
            user = User(
                full_name=u["full_name"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                role=u["role"]
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            if u["role"] == "teacher":
                teacher = user
            print(f"   ✅ Created {u['role']}: {u['email']}")

        if not teacher:
            print("❌ Teacher not found! Exiting.")
            return

        # ── Create Courses ──
        print(f"\n📚 Creating {len(COURSES)} courses...")
        for course_data in COURSES:
            exists = db.query(Course).filter(
                Course.title == course_data["title"]
            ).first()
            if exists:
                print(f"   ⚠️  Course already exists: {course_data['title']}")
                continue

            # Create course
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

            # Create lessons
            for i, lesson_data in enumerate(course_data["lessons"]):
                lesson = Lesson(
                    course_id=course.id,
                    title=lesson_data["title"],
                    content=lesson_data["content"],
                    order_index=i + 1,
                    duration_minutes=lesson_data["duration_minutes"]
                )
                db.add(lesson)

            db.commit()

            # Create quizzes and questions
            for quiz_data in course_data["quizzes"]:
                quiz = Quiz(
                    course_id=course.id,
                    title=quiz_data["title"],
                    pass_marks=quiz_data["pass_marks"],
                    total_marks=len(quiz_data["questions"]),
                    time_limit_minutes=15
                )
                db.add(quiz)
                db.commit()
                db.refresh(quiz)

                for q in quiz_data["questions"]:
                    question = Question(
                        quiz_id=quiz.id,
                        question_text=q["q"],
                        option_a=q["a"],
                        option_b=q["b"],
                        option_c=q["c"],
                        option_d=q["d"],
                        correct_option=q["ans"],
                        marks=1
                    )
                    db.add(question)

                db.commit()

            print(f"   ✅ {course_data['title']} — {len(course_data['lessons'])} lessons, {len(course_data['quizzes'])} quizzes")

        # ── Summary ──
        total_courses = db.query(Course).count()
        total_quizzes = db.query(Quiz).count()
        total_questions = db.query(Question).count()
        total_lessons = db.query(Lesson).count()

        print("\n" + "=" * 50)
        print("🎉 SEED COMPLETE!")
        print("=" * 50)
        print(f"👤 Users:     {db.query(User).count()}")
        print(f"📚 Courses:   {total_courses}")
        print(f"📖 Lessons:   {total_lessons}")
        print(f"📝 Quizzes:   {total_quizzes}")
        print(f"❓ Questions: {total_questions}")
        print("\n🔑 Login Credentials:")
        print("   Teacher → teacher@smartlms.com / teacher123")
        print("   Admin   → admin@smartlms.com / admin123")
        print("\n🌐 Open your app and browse courses!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()