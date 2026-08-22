"""
Automated Verification Test Suite
=================================
Tests all 11 phases of the AI-Powered Resume Analyzer and Job Recommendation System.
Run with: python test_app.py
"""

import os
import sys
import unittest
import json

from app import create_app
from database.connection import db
from database.seed_data import seed_database
from models.user import User
from models.resume import Resume
from models.skill import Skill
from models.job import Job, JobSkill
from models.recommendation import Recommendation
from models.learning_resource import LearningResource

from utils.file_parser import parse_resume_file
from utils.nlp_extractor import nlp_extractor
from utils.ml_matcher import job_matcher
from utils.skill_gap import analyze_skill_gap_for_job
from utils.scoring import calculate_resume_completeness
from utils.learning_engine import get_learning_recommendations_for_skills


class TestResumeAnalyzer(unittest.TestCase):
    """Full End-to-End Project Test Suite."""

    @classmethod
    def setUpClass(cls):
        """Set up Flask test application and in-memory/test database."""
        cls.app = create_app("development")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()
            seed_database()

    # -------------------------------------------------------------
    # Phase 1 & 2: Database Models & Seed Data
    # -------------------------------------------------------------
    def test_01_database_and_models(self):
        """Test database tables and seeded master records."""
        with self.app.app_context():
            self.assertGreaterEqual(User.query.count(), 2)
            self.assertGreaterEqual(Skill.query.count(), 30)
            self.assertGreaterEqual(Job.query.count(), 6)
            self.assertGreaterEqual(LearningResource.query.count(), 15)

    # -------------------------------------------------------------
    # Phase 3: User Authentication & Password Hashing
    # -------------------------------------------------------------
    def test_02_user_auth_and_hashing(self):
        """Test user creation, password hashing, and verification."""
        with self.app.app_context():
            student = User.query.filter_by(email="student@demo.com").first()
            self.assertIsNotNone(student)
            self.assertTrue(student.check_password("password123"))
            self.assertFalse(student.check_password("wrongpass"))
            self.assertEqual(student.role, "student")
            self.assertFalse(student.is_admin)

            admin = User.query.filter_by(email="admin@demo.com").first()
            self.assertIsNotNone(admin)
            self.assertTrue(admin.check_password("admin123"))
            self.assertTrue(admin.is_admin)

    # -------------------------------------------------------------
    # Phase 4: Resume Upload & File Parsing
    # -------------------------------------------------------------
    def test_03_file_parsing(self):
        """Test plain text resume parsing from sample_resumes."""
        sample_path = os.path.join(os.path.dirname(__file__), "sample_resumes", "python_developer_resume.txt")
        self.assertTrue(os.path.exists(sample_path))
        text = parse_resume_file(sample_path)
        self.assertIn("Python", text)
        self.assertIn("Flask", text)
        self.assertIn("ARAVIND", text)

    # -------------------------------------------------------------
    # Phase 5: NLP Skill Extraction
    # -------------------------------------------------------------
    def test_04_nlp_skill_extraction(self):
        """Test NLP extraction across categories and entities."""
        sample_text = """
        John Doe
        Email: john.doe@email.com | Phone: 9876543210
        Education: Bachelor of Engineering in Computer Science (B.E. CSE), 2024
        Experience: 2 years of experience in backend development
        Skills: Python, Flask, Django, MySQL, Docker, Git, REST API, Problem Solving
        """
        result = nlp_extractor.full_parse(sample_text)
        
        self.assertEqual(result["contact"]["email"], "john.doe@email.com")
        self.assertEqual(result["contact"]["phone"], "9876543210")
        self.assertIn("Python", result["skills"]["programming_languages"])
        self.assertIn("Flask", result["skills"]["frameworks"])
        self.assertIn("MySQL", result["skills"]["databases"])
        self.assertIn("Docker", result["skills"]["tools"])
        self.assertIn("Problem Solving", result["skills"]["soft_skills"])

    # -------------------------------------------------------------
    # Phase 7: Machine Learning Matcher (TF-IDF + Cosine Similarity)
    # -------------------------------------------------------------
    def test_05_ml_job_matching(self):
        """Test TF-IDF and Cosine Similarity job recommendations."""
        resume_text = "Proficient in Python, Flask, MySQL, Docker, REST API, Git, Redis."
        skills = ["Python", "Flask", "MySQL", "Docker", "REST API", "Git", "Redis"]

        with self.app.app_context():
            all_jobs = [j.to_dict() for j in Job.query.all()]
            matches = job_matcher.match_resume_to_jobs(resume_text, skills, all_jobs)

            self.assertGreater(len(matches), 0)
            # The top matched role should be Python Backend Developer
            top_match = matches[0]
            self.assertEqual(top_match["title"], "Python Backend Developer")
            self.assertGreaterEqual(top_match["match_percentage"], 60.0)

    # -------------------------------------------------------------
    # Phase 8: Skill Gap Analysis
    # -------------------------------------------------------------
    def test_06_skill_gap_analysis(self):
        """Test skill gap set difference calculation."""
        candidate_skills = ["Python", "Flask", "MySQL"]

        with self.app.app_context():
            job = Job.query.filter_by(title="Python Backend Developer").first()
            self.assertIsNotNone(job)

            gap_result = analyze_skill_gap_for_job(candidate_skills, job)
            self.assertIn("Python", gap_result["matched_skills"])
            self.assertIn("Flask", gap_result["matched_skills"])
            self.assertIn("Docker", gap_result["missing_skills"])
            self.assertIn("Git", gap_result["missing_skills"])
            self.assertGreater(gap_result["gap_percentage"], 0.0)

    # -------------------------------------------------------------
    # Phase 10: Resume Completeness Scoring
    # -------------------------------------------------------------
    def test_07_resume_completeness_scoring(self):
        """Test completeness score calculation and tips."""
        sample_text = "Aravind. Email: a@b.com, Phone: 9876543210. Skills: Python, Flask, MySQL. Education: B.E. Computer Science."
        nlp_result = nlp_extractor.full_parse(sample_text)
        scoring = calculate_resume_completeness(nlp_result, sample_text)

        self.assertGreater(scoring["overall_score"], 0)
        self.assertIn("breakdown", scoring)
        self.assertIn("contact_score", scoring["breakdown"])
        self.assertIn("skills_score", scoring["breakdown"])

    # -------------------------------------------------------------
    # Phase 11: Free Learning Resource Recommendations
    # -------------------------------------------------------------
    def test_08_learning_recommendations(self):
        """Test learning course queries for missing skills."""
        missing = ["Docker", "Kubernetes", "AWS"]

        with self.app.app_context():
            learning_paths = get_learning_recommendations_for_skills(missing)
            self.assertEqual(len(learning_paths), 3)
            docker_path = next(p for p in learning_paths if p["skill_name"] == "Docker")
            self.assertGreaterEqual(len(docker_path["resources"]), 1)
            self.assertTrue(docker_path["resources"][0]["is_free"])

    # -------------------------------------------------------------
    # HTTP Route Endpoints Verification
    # -------------------------------------------------------------
    def test_09_http_routes(self):
        """Test public endpoints and REST API."""
        # 1. Landing Page
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

        # 2. Login Page
        res = self.client.get("/login")
        self.assertEqual(res.status_code, 200)

        # 3. Job Catalog
        res = self.client.get("/jobs")
        self.assertEqual(res.status_code, 200)

        # 4. Learning Hub
        res = self.client.get("/learning")
        self.assertEqual(res.status_code, 200)

        # 5. REST API Health Check
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "healthy")

        # 6. REST API Skills Check
        res = self.client.get("/api/skills")
        self.assertEqual(res.status_code, 200)

        # 7. REST API Analyze Text
        payload = {"text": "Skilled in Python, Flask, MySQL, Machine Learning, Git, and Docker."}
        res = self.client.post("/api/analyze-text", json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("top_recommendations", data)


if __name__ == "__main__":
    unittest.main()
