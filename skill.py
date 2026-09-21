"""
Skill Model
===========
Master repository of technical, tool, framework, database, and soft skills.
"""

from database.connection import db

class Skill(db.Model):
    __tablename__ = "skills"

    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    skill_category = db.Column(
        db.String(50), 
        nullable=False, 
        default="programming_languages"
    )  # programming_languages, frameworks, databases, tools, domain, soft_skills

    # Relationships
    job_associations = db.relationship("JobSkill", backref="skill", lazy=True, cascade="all, delete-orphan")
    learning_resources = db.relationship("LearningResource", backref="skill", lazy=True, cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "skill_category": self.skill_category
        }

    def __repr__(self):
        return f"<Skill {self.skill_name} ({self.skill_category})>"
