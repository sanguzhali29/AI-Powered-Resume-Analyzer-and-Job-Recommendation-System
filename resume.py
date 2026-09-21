"""
Resume Model
============
Stores metadata, extracted raw text, extracted skills, and completeness score
for uploaded resumes.
"""

from datetime import datetime
import json
from database.connection import db

class Resume(db.Model):
    __tablename__ = "resumes"

    resume_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    resume_title = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # 'pdf', 'docx', 'txt'
    extracted_text = db.Column(db.Text, nullable=True)
    extracted_skills = db.Column(db.Text, nullable=True)  # JSON serialized string of skills & categories
    completeness_score = db.Column(db.Float, default=0.0)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    recommendations = db.relationship("Recommendation", backref="resume", lazy=True, cascade="all, delete-orphan")

    def get_skills_dict(self) -> dict:
        """Parses the JSON serialized extracted_skills column."""
        if not self.extracted_skills:
            return {}
        try:
            return json.loads(self.extracted_skills)
        except Exception:
            return {}

    def get_all_skills_flat(self) -> list:
        """Returns a flat list of unique skills detected in the resume."""
        skills_dict = self.get_skills_dict()
        flat_skills = []
        for category, skill_list in skills_dict.items():
            if isinstance(skill_list, list):
                flat_skills.extend(skill_list)
        return list(dict.fromkeys(flat_skills))

    def to_dict(self) -> dict:
        """Serializes the resume model."""
        return {
            "resume_id": self.resume_id,
            "user_id": self.user_id,
            "resume_title": self.resume_title,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "completeness_score": round(self.completeness_score, 1) if self.completeness_score else 0.0,
            "uploaded_at": self.uploaded_at.strftime("%Y-%m-%d %H:%M:%S") if self.uploaded_at else None,
            "skills": self.get_skills_dict(),
            "flat_skills": self.get_all_skills_flat()
        }

    def __repr__(self):
        return f"<Resume {self.resume_title} (ID: {self.resume_id})>"
