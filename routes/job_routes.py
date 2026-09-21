"""
Job Management & Catalog Routes (Phase 6)
=========================================
Handles job listings, role details, search/filter capabilities,
and Admin CRUD operations for job postings and skill weights.
"""

from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, flash, g
)
from database.connection import db
from models.job import Job, JobSkill
from models.skill import Skill
from routes.auth_routes import login_required, admin_required

job_bp = Blueprint("job", __name__)


@job_bp.route("/jobs")
def list_jobs():
    """Public / Student catalog of all available job roles."""
    search_query = request.args.get("q", "").strip()
    industry_filter = request.args.get("industry", "").strip()

    query = Job.query
    if search_query:
        query = query.filter(
            (Job.title.ilike(f"%{search_query}%")) | 
            (Job.description.ilike(f"%{search_query}%")) |
            (Job.company.ilike(f"%{search_query}%"))
        )
    if industry_filter:
        query = query.filter(Job.industry == industry_filter)

    jobs = query.order_by(Job.created_at.desc()).all()
    
    # Get unique industries for filter dropdown
    industries = [
        ind[0] for ind in db.session.query(Job.industry).distinct().all() if ind[0]
    ]

    return render_template(
        "jobs/list.html",
        jobs=jobs,
        search_query=search_query,
        industry_filter=industry_filter,
        industries=sorted(industries)
    )


@job_bp.route("/jobs/<int:job_id>")
def job_detail(job_id: int):
    """Detailed view for a specific job posting."""
    job = Job.query.get_or_404(job_id)
    return render_template("jobs/detail.html", job=job)


@job_bp.route("/admin/jobs/manage")
@admin_required
def manage_jobs():
    """Admin interface for managing all job postings."""
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    skills = Skill.query.order_by(Skill.skill_name.asc()).all()
    return render_template("jobs/manage.html", jobs=jobs, skills=skills)


@job_bp.route("/admin/jobs/create", methods=["POST"])
@admin_required
def create_job():
    """Admin endpoint to create a new job role with required skills."""
    title = request.form.get("title", "").strip()
    company = request.form.get("company", "TechCorp Solutions").strip()
    industry = request.form.get("industry", "Information Technology").strip()
    experience_level = request.form.get("experience_level", "0-2 Years").strip()
    salary_range = request.form.get("salary_range", "6 - 10 LPA").strip()
    description = request.form.get("description", "").strip()
    skill_ids = request.form.getlist("skill_ids")

    if not title or not description:
        flash("Job Title and Description are required.", "danger")
        return redirect(url_for("job.manage_jobs"))

    new_job = Job(
        title=title,
        company=company,
        industry=industry,
        experience_level=experience_level,
        salary_range=salary_range,
        description=description
    )
    db.session.add(new_job)
    db.session.flush()

    for sid in skill_ids:
        try:
            skill_id_int = int(sid)
            js = JobSkill(
                job_id=new_job.job_id,
                skill_id=skill_id_int,
                importance_level="mandatory",
                weight=1.0
            )
            db.session.add(js)
        except ValueError:
            continue

    db.session.commit()
    flash(f"Job posting '{title}' created successfully!", "success")
    return redirect(url_for("job.manage_jobs"))


@job_bp.route("/admin/jobs/delete/<int:job_id>", methods=["POST"])
@admin_required
def delete_job(job_id: int):
    """Admin endpoint to delete a job posting."""
    job = Job.query.get_or_404(job_id)
    title = job.title
    db.session.delete(job)
    db.session.commit()
    flash(f"Job '{title}' has been deleted.", "info")
    return redirect(url_for("job.manage_jobs"))
