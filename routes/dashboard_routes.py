"""
Dashboard & Analytics Routes (Phase 9)
======================================
Provides candidate dashboard and administrative analytics portals.
"""

from flask import (
    Blueprint, render_template, redirect, 
    url_for, flash, g
)
from collections import Counter
import json
from database.connection import db
from models.user import User
from models.resume import Resume
from models.job import Job
from models.recommendation import Recommendation
from models.skill import Skill
from routes.auth_routes import login_required, admin_required
from utils.nlp_extractor import nlp_extractor
from utils.scoring import calculate_resume_completeness

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def user_dashboard():
    """Candidate/Student personalized dashboard."""
    if g.user.is_admin:
        return redirect(url_for("dashboard.admin_dashboard"))

    # Fetch all resumes for the logged-in student
    user_resumes = (
        Resume.query.filter_by(user_id=g.user.user_id)
        .order_by(Resume.uploaded_at.desc())
        .all()
    )

    latest_resume = user_resumes[0] if user_resumes else None
    latest_recommendations = []
    score_analysis = None
    skills_dict = {}

    if latest_resume:
        latest_recommendations = (
            Recommendation.query.filter_by(resume_id=latest_resume.resume_id)
            .order_by(Recommendation.match_percentage.desc())
            .limit(4)
            .all()
        )
        skills_dict = latest_resume.get_skills_dict()
        nlp_result = nlp_extractor.full_parse(latest_resume.extracted_text or "")
        score_analysis = calculate_resume_completeness(nlp_result, latest_resume.extracted_text or "")

    return render_template(
        "dashboard/user_dashboard.html",
        user_resumes=user_resumes,
        latest_resume=latest_resume,
        latest_recommendations=latest_recommendations,
        score_analysis=score_analysis,
        skills_dict=skills_dict
    )


@dashboard_bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    """Administrator analytics portal with system-wide statistics."""
    total_users = User.query.filter_by(role="student").count()
    total_admins = User.query.filter_by(role="admin").count()
    total_resumes = Resume.query.count()
    total_jobs = Job.query.count()
    total_skills = Skill.query.count()

    # Calculate skill frequency across all uploaded resumes
    all_resumes = Resume.query.all()
    skill_frequency = Counter()
    for res in all_resumes:
        for sk in res.get_all_skills_flat():
            skill_frequency[sk] += 1

    top_skills = skill_frequency.most_common(10)
    top_skill_labels = [s[0] for s in top_skills]
    top_skill_counts = [s[1] for s in top_skills]

    # Recent resumes & users
    recent_resumes = Resume.query.order_by(Resume.uploaded_at.desc()).limit(8).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(8).all()

    return render_template(
        "dashboard/admin_dashboard.html",
        total_users=total_users,
        total_admins=total_admins,
        total_resumes=total_resumes,
        total_jobs=total_jobs,
        total_skills=total_skills,
        top_skills=top_skills,
        top_skill_labels_json=json.dumps(top_skill_labels),
        top_skill_counts_json=json.dumps(top_skill_counts),
        recent_resumes=recent_resumes,
        recent_users=recent_users
    )
