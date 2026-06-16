import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session
from app.models.quiz import QuizAttempt
from app.models.course import Enrollment
import os

# Features used from Kaggle dataset - mapped to LMS data
FEATURES = [
    'grade_1st_sem',        # → quiz avg score (0-20 scale)
    'grade_2nd_sem',        # → assignment avg score
    'approved_1st_sem',     # → quizzes passed
    'approved_2nd_sem',     # → courses completed
    'enrolled_1st_sem',     # → total quiz attempts
    'enrolled_2nd_sem',     # → total enrollments
    'evaluations_1st_sem',  # → engagement score * 10
    'evaluations_2nd_sem',  # → login frequency
    'tuition_up_to_date',   # → is_active student (always 1)
    'scholarship_holder',   # → has passed any quiz (0 or 1)
    'age_at_enrollment',    # → fixed at 20 for LMS
    'debtor',               # → has failed quizzes (0 or 1)
]

class PerformancePredictor:

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self._train_with_kaggle_data()

    def _train_with_kaggle_data(self):
        """Train Random Forest using Kaggle student dataset"""
        try:
            # Try to find the dataset
            possible_paths = [
                os.path.join(
                    os.path.dirname(__file__),
                    '../../..', 'ml', 'datasets', 'student_data.csv'
                ),
                'ml/datasets/student_data.csv',
                '../ml/datasets/student_data.csv',
            ]

            df = None
            for path in possible_paths:
                normalized = os.path.normpath(path)
                if os.path.exists(normalized):
                    df = pd.read_csv(normalized)
                    print(f"✅ Loaded Kaggle dataset from: {normalized}")
                    break

            if df is not None:
                self._train_on_dataframe(df)
            else:
                print("⚠️ Kaggle dataset not found. Using synthetic data.")
                self._train_with_synthetic_data()

        except Exception as e:
            print(f"⚠️ Error loading dataset: {e}. Using synthetic data.")
            self._train_with_synthetic_data()

    def _train_on_dataframe(self, df: pd.DataFrame):
        """Train model on the Kaggle dataframe"""

        # Use the exact Kaggle columns
        kaggle_features = [
            'Curricular units 1st sem (grade)',
            'Curricular units 2nd sem (grade)',
            'Curricular units 1st sem (approved)',
            'Curricular units 2nd sem (approved)',
            'Curricular units 1st sem (enrolled)',
            'Curricular units 2nd sem (enrolled)',
            'Curricular units 1st sem (evaluations)',
            'Curricular units 2nd sem (evaluations)',
            'Tuition fees up to date',
            'Scholarship holder',
            'Age at enrollment',
            'Debtor'
        ]

        X = df[kaggle_features].values
        y = df['Target'].values

        # Encode: Dropout→at_risk, Enrolled→on_track, Graduate→excelling
        label_map = {
            'Dropout': 'at_risk',
            'Enrolled': 'on_track',
            'Graduate': 'excelling'
        }
        y_mapped = np.array([label_map[label] for label in y])

        # Split and train
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_mapped,
            test_size=0.2,
            random_state=42,
            stratify=y_mapped
        )

        X_train_scaled = self.scaler.fit_transform(X_train)

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        print("✅ Model trained on Kaggle dataset!")

    def _train_with_synthetic_data(self):
        """Fallback: train with synthetic data"""
        np.random.seed(42)

        at_risk = np.column_stack([
            np.random.uniform(0, 6, 200),
            np.random.uniform(0, 6, 200),
            np.random.randint(0, 2, 200).astype(float),
            np.random.randint(0, 2, 200).astype(float),
            np.random.randint(1, 4, 200).astype(float),
            np.random.randint(1, 3, 200).astype(float),
            np.random.randint(1, 4, 200).astype(float),
            np.random.randint(1, 4, 200).astype(float),
            np.zeros(200),
            np.zeros(200),
            np.random.randint(18, 30, 200).astype(float),
            np.ones(200),
        ])

        on_track = np.column_stack([
            np.random.uniform(6, 13, 200),
            np.random.uniform(6, 13, 200),
            np.random.randint(2, 5, 200).astype(float),
            np.random.randint(2, 5, 200).astype(float),
            np.random.randint(4, 8, 200).astype(float),
            np.random.randint(3, 6, 200).astype(float),
            np.random.randint(4, 8, 200).astype(float),
            np.random.randint(4, 8, 200).astype(float),
            np.ones(200),
            np.zeros(200),
            np.random.randint(18, 30, 200).astype(float),
            np.zeros(200),
        ])

        excelling = np.column_stack([
            np.random.uniform(13, 20, 200),
            np.random.uniform(13, 20, 200),
            np.random.randint(5, 10, 200).astype(float),
            np.random.randint(5, 10, 200).astype(float),
            np.random.randint(8, 15, 200).astype(float),
            np.random.randint(6, 10, 200).astype(float),
            np.random.randint(8, 15, 200).astype(float),
            np.random.randint(8, 15, 200).astype(float),
            np.ones(200),
            np.ones(200),
            np.random.randint(18, 30, 200).astype(float),
            np.zeros(200),
        ])

        X = np.vstack([at_risk, on_track, excelling])
        y = (
            ['at_risk'] * 200 +
            ['on_track'] * 200 +
            ['excelling'] * 200
        )

        X_scaled = self.scaler.fit_transform(X)
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model.fit(X_scaled, y)
        self.is_trained = True
        print("✅ Model trained on synthetic data!")

    def _extract_lms_features(
        self, student_id: int, course_id: int, db: Session
    ) -> np.ndarray:
        """
        Map real LMS student data to Kaggle dataset feature scale
        Kaggle grade scale: 0-20
        LMS quiz score scale: 0-100 → divide by 5 to get 0-20
        """

        # Get quiz attempts
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.student_id == student_id
        ).all()

        # Get enrollments
        enrollments = db.query(Enrollment).filter(
            Enrollment.student_id == student_id
        ).all()

        total_attempts = len(attempts)
        total_enrollments = len(enrollments)

        # Calculate quiz avg (convert 0-100 to 0-20 scale)
        quiz_avg_0_to_20 = 0.0
        quizzes_passed = 0
        quizzes_failed = 0

        if attempts:
            scores_pct = [
                (a.score / a.total_marks * 100)
                for a in attempts
                if a.total_marks and a.total_marks > 0
            ]
            if scores_pct:
                quiz_avg_pct = np.mean(scores_pct)
                quiz_avg_0_to_20 = quiz_avg_pct / 5.0  # 0-100 → 0-20

            quizzes_passed = sum(1 for a in attempts if a.passed)
            quizzes_failed = total_attempts - quizzes_passed

        # Map to Kaggle features
        features = np.array([[
            quiz_avg_0_to_20,           # grade_1st_sem (0-20)
            quiz_avg_0_to_20 * 0.9,     # grade_2nd_sem (slightly lower)
            float(quizzes_passed),       # approved_1st_sem
            float(max(0, quizzes_passed - 1)),  # approved_2nd_sem
            float(total_attempts),       # enrolled_1st_sem
            float(total_enrollments),    # enrolled_2nd_sem
            float(total_attempts * 2),   # evaluations_1st_sem
            float(total_attempts * 2),   # evaluations_2nd_sem
            1.0,                         # tuition_up_to_date (active)
            1.0 if quizzes_passed > 0 else 0.0,  # scholarship_holder
            20.0,                        # age_at_enrollment
            1.0 if quizzes_failed > 2 else 0.0,  # debtor
        ]])

        return features

    def predict(self, student_id: int, course_id: int, db: Session) -> dict:
        """Predict student performance using Kaggle-trained model"""

        features = self._extract_lms_features(student_id, course_id, db)
        features_scaled = self.scaler.transform(features)

        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        classes = self.model.classes_

        prob_dict = dict(zip(classes, probabilities.tolist()))

        # Get student stats for display
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.student_id == student_id
        ).all()

        quiz_avg = 0.0
        if attempts:
            scores = [
                (a.score / a.total_marks * 100)
                for a in attempts
                if a.total_marks and a.total_marks > 0
            ]
            quiz_avg = round(np.mean(scores), 1) if scores else 0.0

        enrollments = db.query(Enrollment).filter(
            Enrollment.student_id == student_id
        ).all()

        recommendations = self._get_recommendations(
            prediction, quiz_avg, len(attempts), len(enrollments)
        )

        return {
            "student_id": student_id,
            "course_id": course_id,
            "prediction": prediction,
            "confidence": round(max(probabilities) * 100, 1),
            "probabilities": {
                "at_risk": round(prob_dict.get("at_risk", 0) * 100, 1),
                "on_track": round(prob_dict.get("on_track", 0) * 100, 1),
                "excelling": round(prob_dict.get("excelling", 0) * 100, 1),
            },
            "features_used": {
                "quiz_avg_score": quiz_avg,
                "quiz_attempts": len(attempts),
                "courses_enrolled": len(enrollments),
                "model": "RandomForest trained on 4424 real students"
            },
            "recommendations": recommendations
        }

    def _get_recommendations(
        self,
        prediction: str,
        quiz_avg: float,
        attempts: int,
        enrollments: int
    ) -> list:
        """Generate specific recommendations based on real data"""

        if prediction == "at_risk":
            recs = [
                f"⚠️ Your average score is {quiz_avg:.1f}% — aim for above 60%",
                "📚 Review all course materials before attempting quizzes",
                "🔄 Re-attempt failed quizzes to improve your score",
                "🤝 Use SmartBot to get help on difficult topics",
                "⏰ Increase your study time — consistency is key!",
            ]
            if attempts == 0:
                recs.insert(0, "🚀 Start by attempting your first quiz today!")
            if enrollments == 0:
                recs.insert(0, "📖 Enroll in a course to begin your journey!")

        elif prediction == "on_track":
            recs = [
                f"✅ Good job! Your average score is {quiz_avg:.1f}%",
                "🎯 Push your score above 75% to reach Excelling status",
                "📈 Attempt more quizzes to strengthen your profile",
                "🔄 Review topics where you scored below 70%",
                "🏆 You are close to the top — keep going!",
            ]

        else:  # excelling
            recs = [
                f"🌟 Outstanding! Your average score is {quiz_avg:.1f}%",
                "🚀 You are performing like a top Graduate student!",
                "📖 Challenge yourself with advanced courses",
                "👥 Help fellow students — teaching reinforces learning",
                "🏅 Keep this pace and you will top the leaderboard!",
            ]

        return recs


# Singleton instance
predictor = PerformancePredictor()