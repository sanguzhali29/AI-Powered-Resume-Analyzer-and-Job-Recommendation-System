"""
Job & JobSkill Models
=====================
Stores job descriptions, company information, industry categories,
and required skill associations with importance weights.
"""

from datetime import datetime
from database.connection import db

class Job(db.Model):
    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False, index=True)
    company = db.Column(db.String(100), nullable=False, default="TechCorp Solutions")
    industry = db.Column(db.String(100), nullable=False, default="Information Technology")
    experience_level = db.Column(db.String(50), default="Entry to Mid Level")
    salary_range = db.Column(db.String(50), default="6 - 12 LPA")
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    job_skills = db.relationship("JobSkill", backref="job", lazy=True, cascade="all, delete-orphan")
    recommendations = db.relationship("Recommendation", backref="job", lazy=True, cascade="all, delete-orphan")

    def get_required_skills(self) -> list:
        """Returns a list of required skill names for this job."""
        return [js.skill.skill_name for js in self.job_skills if js.skill]

    def get_mandatory_skills(self) -> list:
        """Returns skills flagged as mandatory."""
        return [js.skill.skill_name for js in self.job_skills if js.importance_level == "mandatory" and js.skill]

    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "industry": self.industry,
            "experience_level": self.experience_level,
            "salary_range": self.salary_range,
            "description": self.description,
            "skills": [
                {
                    "skill_id": js.skill_id,
                    "skill_name": js.skill.skill_name if js.skill else "",
                    "category": js.skill.skill_category if js.skill else "",
                    "importance": js.importance_level,
                    "weight": float(js.weight)
                }
                for js in self.job_skills
            ],
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }

    def __repr__(self):
        return f"<Job {self.title} at {self.company}>"


class JobSkill(db.Model):
    __tablename__ = "job_skills"

    job_skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)
    importance_level = db.Column(db.String(20), default="mandatory")  # mandatory, important, good_to_have
    weight = db.Column(db.Float, default=1.0)

    __table_args__ = (
        db.UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),
    )

    def __repr__(self):
        return f"<JobSkill JobID:{self.job_id} SkillID:{self.skill_id} ({self.importance_level})>"
