import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.models.course import Course, Enrollment
from app.models.quiz import QuizAttempt

class RecommendationEngine:

    def get_recommendations(self, student_id: int, db: Session, top_n: int = 5):
        """
        Hybrid recommendation: content-based + collaborative filtering
        """
        # Get all courses
        all_courses = db.query(Course).filter(Course.is_published == True).all()
        if not all_courses:
            return []

        # Get student's enrolled course IDs
        enrolled = db.query(Enrollment).filter(
            Enrollment.student_id == student_id
        ).all()
        enrolled_course_ids = {e.course_id for e in enrolled}

        # Get unenrolled courses
        unenrolled = [c for c in all_courses if c.id not in enrolled_course_ids]
        if not unenrolled:
            return []

        # Score each unenrolled course
        scored_courses = []
        for course in unenrolled:
            score = self._calculate_score(
                course, student_id, enrolled_course_ids, db
            )
            scored_courses.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "category": course.category,
                "difficulty_level": course.difficulty_level,
                "recommendation_score": round(score, 3)
            })

        # Sort by score descending
        scored_courses.sort(
            key=lambda x: x["recommendation_score"], reverse=True
        )
        return scored_courses[:top_n]

    def _calculate_score(
        self, course, student_id: int,
        enrolled_ids: set, db: Session
    ) -> float:
        score = 0.0

        # Factor 1: Category match with enrolled courses (40%)
        if enrolled_ids:
            enrolled_courses = db.query(Course).filter(
                Course.id.in_(enrolled_ids)
            ).all()
            enrolled_categories = {c.category for c in enrolled_courses if c.category}
            if course.category in enrolled_categories:
                score += 0.4

        # Factor 2: Popularity (how many students enrolled) (30%)
        enrollment_count = db.query(Enrollment).filter(
            Enrollment.course_id == course.id
        ).count()
        popularity_score = min(enrollment_count / 10.0, 1.0)
        score += popularity_score * 0.3

        # Factor 3: Difficulty progression (30%)
        difficulty_order = {"beginner": 1, "intermediate": 2, "advanced": 3}
        if enrolled_ids:
            enrolled_courses = db.query(Course).filter(
                Course.id.in_(enrolled_ids)
            ).all()
            avg_difficulty = np.mean([
                difficulty_order.get(c.difficulty_level, 1)
                for c in enrolled_courses
            ]) if enrolled_courses else 1

            course_difficulty = difficulty_order.get(course.difficulty_level, 1)

            # Prefer next level difficulty
            if course_difficulty == int(avg_difficulty) + 1:
                score += 0.3
            elif course_difficulty == int(avg_difficulty):
                score += 0.15
        else:
            # New student → recommend beginner courses
            if course.difficulty_level == "beginner":
                score += 0.3

        return score

    def get_collaborative_recommendations(
        self, student_id: int, db: Session, top_n: int = 5
    ):
        """
        Collaborative filtering: find similar students
        and recommend what they enrolled in
        """
        # Build student-course matrix
        all_enrollments = db.query(Enrollment).all()
        if not all_enrollments:
            return []

        # Create matrix data
        data = [(e.student_id, e.course_id) for e in all_enrollments]
        df = pd.DataFrame(data, columns=["student_id", "course_id"])

        if student_id not in df["student_id"].values:
            return []

        # Pivot table: rows=students, cols=courses, values=1 if enrolled
        matrix = df.pivot_table(
            index="student_id",
            columns="course_id",
            aggfunc=lambda x: 1,
            fill_value=0
        )

        if student_id not in matrix.index:
            return []

        # Compute cosine similarity between students
        similarity = cosine_similarity(matrix)
        sim_df = pd.DataFrame(
            similarity,
            index=matrix.index,
            columns=matrix.index
        )

        # Get top 3 similar students
        similar_students = sim_df[student_id].drop(student_id).nlargest(3).index.tolist()

        # Find courses those students enrolled in but current student hasn't
        student_courses = set(
            matrix.loc[student_id][matrix.loc[student_id] == 1].index
        )
        recommended_course_ids = set()

        for sim_student in similar_students:
            if sim_student in matrix.index:
                sim_courses = set(
                    matrix.loc[sim_student][matrix.loc[sim_student] == 1].index
                )
                recommended_course_ids.update(sim_courses - student_courses)

        # Fetch course details
        recommendations = []
        for course_id in list(recommended_course_ids)[:top_n]:
            course = db.query(Course).filter(
                Course.id == course_id,
                Course.is_published == True
            ).first()
            if course:
                recommendations.append({
                    "id": course.id,
                    "title": course.title,
                    "description": course.description,
                    "category": course.category,
                    "difficulty_level": course.difficulty_level,
                    "recommendation_score": 0.85
                })

        return recommendations


recommendation_engine = RecommendationEngine()