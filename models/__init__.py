"""
Models Package Initialization
=============================
Exports all SQLAlchemy ORM models for easy import across routes, services, and tests.
"""

from models.user import User
from models.resume import Resume
from models.skill import Skill
from models.job import Job, JobSkill
from models.recommendation import Recommendation
from models.learning_resource import LearningResource

__all__ = [
    "User",
    "Resume",
    "Skill",
    "Job",
    "JobSkill",
    "Recommendation",
    "LearningResource",
]
