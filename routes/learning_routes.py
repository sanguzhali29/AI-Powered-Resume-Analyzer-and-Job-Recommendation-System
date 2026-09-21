"""
Learning Recommendation Routes (Phase 11)
=========================================
Delivers personalized free course recommendations and interactive tutorials
for identified skill gaps.
"""

from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, flash, g
)
from models.resume import Resume
from models.job import Job
from models.skill import Skill
from models.learning_resource import LearningResource
from models.recommendation import Recommendation
from routes.auth_routes import login_required
from utils.learning_engine import get_learning_recommendations_for_skills
from utils.skill_gap import analyze_skill_gap_for_job

learning_bp = Blueprint("learning", __name__)


@learning_bp.route("/learning")
def learning_hub():
    """Exploration hub of all curated free learning resources in the system."""
    category_filter = request.args.get("category", "").strip()
    search_query = request.args.get("q", "").strip()

    query = LearningResource.query.join(Skill)
    if category_filter:
        query = query.filter(Skill.skill_category == category_filter)
    if search_query:
        query = query.filter(
            (LearningResource.title.ilike(f"%{search_query}%")) |
            (Skill.skill_name.ilike(f"%{search_query}%")) |
            (LearningResource.platform.ilike(f"%{search_query}%"))
        )

    resources = query.order_by(Skill.skill_name.asc()).all()
    categories = [
        "programming_languages", "frameworks", "databases", "tools", "domain", "soft_skills"
    ]

    return render_template(
        "learning/resources.html",
        resources=resources,
        categories=categories,
        active_category=category_filter,
        search_query=search_query,
        is_personalized=False
    )


@learning_bp.route("/learning/path/<int:resume_id>")
@login_required
def personalized_learning_path(resume_id: int):
    """
    Generates a tailored learning roadmap for missing skills corresponding
    to the candidate's selected or top-matched job role.
    """
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != g.user.user_id and not g.user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("dashboard.user_dashboard"))

    job_id = request.args.get("job_id", type=int)
    target_job = None
    if job_id:
        target_job = Job.query.get(job_id)

    if not target_job:
        top_rec = (
            Recommendation.query.filter_by(resume_id=resume_id)
            .order_by(Recommendation.match_percentage.desc())
            .first()
        )
        if top_rec and top_rec.job:
            target_job = top_rec.job
        else:
            target_job = Job.query.first()

    candidate_skills = resume.get_all_skills_flat()
    gap_data = analyze_skill_gap_for_job(candidate_skills, target_job)
    missing_skills = gap_data["missing_skills"]

    learning_paths = get_learning_recommendations_for_skills(missing_skills)

    return render_template(
        "learning/resources.html",
        resume=resume,
        target_job=target_job,
        gap_data=gap_data,
        learning_paths=learning_paths,
        is_personalized=True
    )
