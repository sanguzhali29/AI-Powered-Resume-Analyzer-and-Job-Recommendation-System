"""
Utils Package Initialization
============================
Exports all helper modules: parsing, NLP extraction, ML matching, gap analysis,
scoring, and learning engine.
"""

from utils.file_parser import parse_resume_file, ResumeParseError
from utils.nlp_extractor import nlp_extractor, NLPExtractor
from utils.ml_matcher import job_matcher, JobMatcher
from utils.skill_gap import analyze_skill_gap_for_job, calculate_global_skill_demand
from utils.scoring import calculate_resume_completeness
from utils.learning_engine import get_learning_recommendations_for_skills

__all__ = [
    "parse_resume_file",
    "ResumeParseError",
    "nlp_extractor",
    "NLPExtractor",
    "job_matcher",
    "JobMatcher",
    "analyze_skill_gap_for_job",
    "calculate_global_skill_demand",
    "calculate_resume_completeness",
    "get_learning_recommendations_for_skills",
]
