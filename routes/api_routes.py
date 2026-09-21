"""
REST API Endpoints Module
=========================
Provides JSON API endpoints for AJAX interactions, programmatic access,
and live resume text analysis.
"""

from flask import Blueprint, request, jsonify
from models.job import Job
from models.skill import Skill
from utils.nlp_extractor import nlp_extractor
from utils.ml_matcher import job_matcher
from utils.skill_gap import analyze_skill_gap_for_job
from utils.scoring import calculate_resume_completeness
from utils.learning_engine import get_learning_recommendations_for_skills

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "AI Resume Analyzer API"}), 200


@api_bp.route("/skills", methods=["GET"])
def get_skills():
    """Returns all master skills grouped by category."""
    skills = Skill.query.order_by(Skill.skill_name.asc()).all()
    grouped = {}
    for s in skills:
        grouped.setdefault(s.skill_category, []).append(s.skill_name)
    return jsonify({"skills": grouped, "total_skills": len(skills)}), 200


@api_bp.route("/jobs", methods=["GET"])
def get_jobs():
    """Returns all active jobs with required skills."""
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return jsonify({"jobs": [j.to_dict() for j in jobs]}), 200


@api_bp.route("/analyze-text", methods=["POST"])
def analyze_text():
    """
    Accepts raw resume text in JSON payload: { "text": "..." }
    Runs NLP extraction, scoring, and job matching asynchronously.
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    
    if not text:
        return jsonify({"error": "No resume text provided in 'text' field."}), 400

    # 1. NLP Extraction
    nlp_result = nlp_extractor.full_parse(text)
    flat_skills = nlp_result["flat_skills"]

    # 2. Completeness Scoring
    scoring = calculate_resume_completeness(nlp_result, text)

    # 3. ML Job Matching
    all_jobs = Job.query.all()
    jobs_dicts = [j.to_dict() for j in all_jobs]
    matches = job_matcher.match_resume_to_jobs(text, flat_skills, jobs_dicts)

    return jsonify({
        "nlp_extraction": nlp_result,
        "scoring": scoring,
        "top_recommendations": matches[:5]
    }), 200


@api_bp.route("/skill-gap", methods=["POST"])
def api_skill_gap():
    """
    Accepts candidate skills and job_id in JSON payload:
    { "candidate_skills": ["Python", "Flask"], "job_id": 1 }
    """
    data = request.get_json(silent=True) or {}
    candidate_skills = data.get("candidate_skills", [])
    job_id = data.get("job_id")

    if not job_id:
        return jsonify({"error": "job_id is required."}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found."}), 404

    gap_data = analyze_skill_gap_for_job(candidate_skills, job)
    learning_resources = get_learning_recommendations_for_skills(gap_data["missing_skills"])

    return jsonify({
        "gap_analysis": gap_data,
        "learning_resources": learning_resources
    }), 200
