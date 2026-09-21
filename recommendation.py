"""
Recommendation Model
====================
Stores historical AI matching scores, matched skills, and missing skills
generated for a specific resume and target job.
"""

from datetime import datetime
import json
from database.connection import db

class Recommendation(db.Model):
    __tablename__ = "recommendations"

    recommendation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False, index=True)
    match_percentage = db.Column(db.Float, nullable=False)
    matched_skills = db.Column(db.Text, nullable=True)  # JSON string of matched skills list
    missing_skills = db.Column(db.Text, nullable=True)  # JSON string of missing skills list
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_matched_skills_list(self) -> list:
        if not self.matched_skills:
            return []
        try:
            return json.loads(self.matched_skills)
        except Exception:
            return [s.strip() for s in self.matched_skills.split(",") if s.strip()]

    def get_missing_skills_list(self) -> list:
        if not self.missing_skills:
            return []
        try:
            return json.loads(self.missing_skills)
        except Exception:
            return [s.strip() for s in self.missing_skills.split(",") if s.strip()]

    def to_dict(self) -> dict:
        return {
            "recommendation_id": self.recommendation_id,
            "resume_id": self.resume_id,
            "job_id": self.job_id,
            "job_title": self.job.title if self.job else "Unknown Job",
            "company": self.job.company if self.job else "",
            "match_percentage": round(self.match_percentage, 1),
            "matched_skills": self.get_matched_skills_list(),
            "missing_skills": self.get_missing_skills_list(),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }

    def __repr__(self):
        return f"<Recommendation Resume:{self.resume_id} Job:{self.job_id} Match:{self.match_percentage}%>"
