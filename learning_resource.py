"""
LearningResource Model
======================
Stores free learning resources (YouTube, freeCodeCamp, Coursera Free, W3Schools,
Official Docs, GeeksforGeeks) linked to specific skill IDs.
"""

from database.connection import db

class LearningResource(db.Model):
    __tablename__ = "learning_resources"

    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    platform = db.Column(
        db.String(50), 
        nullable=False, 
        default="YouTube"
    )  # YouTube, freeCodeCamp, Coursera Free, W3Schools, Official Docs, GeeksforGeeks
    resource_type = db.Column(
        db.String(50), 
        default="Video Course"
    )  # Video Course, Interactive Tutorial, Documentation, Article
    duration_hours = db.Column(db.String(30), default="5-10 Hours")
    is_free = db.Column(db.Boolean, default=True)

    def to_dict(self) -> dict:
        return {
            "resource_id": self.resource_id,
            "skill_id": self.skill_id,
            "skill_name": self.skill.skill_name if self.skill else "",
            "title": self.title,
            "url": self.url,
            "platform": self.platform,
            "resource_type": self.resource_type,
            "duration_hours": self.duration_hours,
            "is_free": self.is_free
        }

    def __repr__(self):
        return f"<LearningResource {self.title} ({self.platform})>"
