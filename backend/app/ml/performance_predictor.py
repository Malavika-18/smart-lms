import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from app.models.quiz import QuizAttempt
from app.models.course import Enrollment

class PerformancePredictor:

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=5
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self._train_with_synthetic_data()

    def _train_with_synthetic_data(self):
        """
        Train with synthetic data until real data is available.
        In production this would use real historical student data.
        """
        np.random.seed(42)
        n_samples = 500

        # Generate synthetic student features
        # [quiz_avg, assignment_avg, login_count, time_spent, engagement]
        at_risk = np.column_stack([
            np.random.uniform(0, 40, 170),    # low quiz scores
            np.random.uniform(0, 45, 170),    # low assignment scores
            np.random.randint(1, 5, 170),     # low login count
            np.random.uniform(10, 60, 170),   # low time spent
            np.random.uniform(0, 0.3, 170),   # low engagement
        ])

        on_track = np.column_stack([
            np.random.uniform(40, 70, 165),   # medium quiz scores
            np.random.uniform(45, 75, 165),   # medium assignment scores
            np.random.randint(5, 15, 165),    # medium login count
            np.random.uniform(60, 180, 165),  # medium time spent
            np.random.uniform(0.3, 0.7, 165), # medium engagement
        ])

        excelling = np.column_stack([
            np.random.uniform(70, 100, 165),  # high quiz scores
            np.random.uniform(75, 100, 165),  # high assignment scores
            np.random.randint(15, 30, 165),   # high login count
            np.random.uniform(180, 400, 165), # high time spent
            np.random.uniform(0.7, 1.0, 165), # high engagement
        ])

        X = np.vstack([at_risk, on_track, excelling])
        y = (
            ["at_risk"] * 170 +
            ["on_track"] * 165 +
            ["excelling"] * 165
        )

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict(self, student_id: int, course_id: int, db: Session) -> dict:
        """Predict student performance for a specific course"""

        # Extract real features from database
        features = self._extract_features(student_id, course_id, db)

        # Scale and predict
        feature_array = np.array([[
            features["quiz_avg_score"],
            features["assignment_avg_score"],
            features["login_count"],
            features["time_spent_minutes"],
            features["engagement_score"]
        ]])

        scaled = self.scaler.transform(feature_array)
        prediction = self.model.predict(scaled)[0]
        probabilities = self.model.predict_proba(scaled)[0]
        classes = self.model.classes_

        prob_dict = dict(zip(classes, probabilities.tolist()))

        # Generate recommendations based on prediction
        recommendations = self._get_recommendations(prediction, features)

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
            "features_used": features,
            "recommendations": recommendations
        }

    def _extract_features(
        self, student_id: int, course_id: int, db: Session
    ) -> dict:
        """Extract real student features from database"""

        # Quiz performance
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
            quiz_avg = np.mean(scores) if scores else 0.0

        # Enrollment engagement
        enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        ).first()

        progress = enrollment.progress_percent if enrollment else 0.0
        engagement = min(progress / 100.0, 1.0)

        return {
            "quiz_avg_score": round(quiz_avg, 2),
            "assignment_avg_score": round(quiz_avg * 0.9, 2),
            "login_count": len(attempts) * 2 + 1,
            "time_spent_minutes": len(attempts) * 30,
            "engagement_score": round(engagement, 3),
            "quiz_attempts": len(attempts),
            "course_progress": round(progress, 1)
        }

    def _get_recommendations(self, prediction: str, features: dict) -> list:
        """Generate actionable recommendations based on prediction"""
        recommendations = []

        if prediction == "at_risk":
            recommendations = [
                "⚠️ Schedule extra study sessions this week",
                "📚 Review all previous quiz mistakes carefully",
                "🤝 Consider joining a study group",
                "💬 Reach out to your teacher for help",
                "⏰ Increase your daily study time to at least 2 hours"
            ]
        elif prediction == "on_track":
            recommendations = [
                "✅ Good progress! Keep up your current pace",
                "🎯 Focus on improving weak topic areas",
                "📈 Try advanced practice problems",
                "🔄 Review older material to strengthen foundations",
                "🏆 Aim for the leaderboard top 10!"
            ]
        else:  # excelling
            recommendations = [
                "🌟 Outstanding performance! Keep it up!",
                "🚀 Consider taking advanced courses",
                "👥 Help your classmates to reinforce your knowledge",
                "🏅 You are on track for top honors",
                "📖 Explore related topics to broaden your skills"
            ]

        return recommendations


predictor = PerformancePredictor()