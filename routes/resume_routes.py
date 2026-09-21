"""
Resume Management & Analysis Routes (Phases 4, 5, 7, 8, 10)
===========================================================
Handles resume uploads, text extraction, NLP skill parsing,
TF-IDF job matching, skill gap calculation, and scoring analysis.
"""

import os
import json
from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, flash, current_app, g, jsonify
)
from werkzeug.utils import secure_filename

from database.connection import db
from models.resume import Resume
from models.job import Job
from models.recommendation import Recommendation
from routes.auth_routes import login_required
from utils.file_parser import parse_resume_file, ResumeParseError
from utils.nlp_extractor import nlp_extractor
from utils.ml_matcher import job_matcher
from utils.skill_gap import analyze_skill_gap_for_job, calculate_global_skill_demand
from utils.scoring import calculate_resume_completeness

resume_bp = Blueprint("resume", __name__)


def allowed_file(filename: str) -> bool:
    """Checks if the uploaded file has an allowed extension."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


@resume_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_resume():
    """Handles resume upload and launches the end-to-end analysis pipeline."""
    if request.method == "POST":
        # Check if file part is present
        if "resume_file" not in request.files:
            flash("No file part in the request.", "danger")
            return redirect(request.url)

        file = request.files["resume_file"]
        resume_title = request.form.get("resume_title", "").strip()

        if file.filename == "":
            flash("No file selected for upload.", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file format. Please upload a PDF, DOCX, or TXT file.", "danger")
            return redirect(request.url)

        # 1. Save uploaded file securely
        filename = secure_filename(file.filename)
        _, ext = os.path.splitext(filename)
        file_ext = ext.lower().replace(".", "")
        
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)
        
        # Unique file naming
        saved_filename = f"user_{g.user.user_id}_{filename}"
        file_path = os.path.join(upload_folder, saved_filename)
        file.save(file_path)

        # 2. Parse Raw Text
        try:
            extracted_text = parse_resume_file(file_path)
        except ResumeParseError as e:
            flash(f"Error parsing resume: {str(e)}", "danger")
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(request.url)

        # 3. NLP Extraction Pipeline
        nlp_result = nlp_extractor.full_parse(extracted_text)
        flat_skills = nlp_result["flat_skills"]

        # 4. Completeness & ATS Scoring
        score_analysis = calculate_resume_completeness(nlp_result, extracted_text)
        completeness_score = score_analysis["overall_score"]

        # 5. Persist Resume in Database
        title = resume_title if resume_title else filename
        new_resume = Resume(
            user_id=g.user.user_id,
            resume_title=title,
            file_path=file_path,
            file_type=file_ext,
            extracted_text=extracted_text,
            extracted_skills=json.dumps(nlp_result["skills"]),
            completeness_score=completeness_score
        )
        db.session.add(new_resume)
        db.session.commit()

        # 6. Run TF-IDF + Cosine Similarity Matching on all active jobs
        all_jobs = Job.query.all()
        jobs_dicts = [j.to_dict() for j in all_jobs]
        ranked_matches = job_matcher.match_resume_to_jobs(
            extracted_text, flat_skills, jobs_dicts
        )

        # 7. Persist Recommendations
        for match in ranked_matches:
            rec = Recommendation(
                resume_id=new_resume.resume_id,
                job_id=match["job_id"],
                match_percentage=match["match_percentage"],
                matched_skills=json.dumps(match["matched_skills"]),
                missing_skills=json.dumps(match["missing_skills"])
            )
            db.session.add(rec)
        db.session.commit()

        flash(f"Resume '{title}' uploaded and analyzed successfully!", "success")
        return redirect(url_for("resume.view_results", resume_id=new_resume.resume_id))

    return render_template("resume/upload.html")


@resume_bp.route("/resume/<int:resume_id>")
@login_required
def view_resume(resume_id: int):
    """Displays in-depth parsed resume information and completeness breakdown."""
    resume = Resume.query.get_or_404(resume_id)
    
    # Ensure user owns this resume or is admin
    if resume.user_id != g.user.user_id and not g.user.is_admin:
        flash("You do not have permission to view this resume.", "danger")
        return redirect(url_for("dashboard.user_dashboard"))

    nlp_result = nlp_extractor.full_parse(resume.extracted_text or "")
    score_analysis = calculate_resume_completeness(nlp_result, resume.extracted_text or "")

    return render_template(
        "resume/view.html",
        resume=resume,
        nlp_result=nlp_result,
        score_analysis=score_analysis
    )


@resume_bp.route("/recommendations/<int:resume_id>")
@login_required
def view_results(resume_id: int):
    """Displays ranked job recommendations and match percentages."""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != g.user.user_id and not g.user.is_admin:
        flash("You do not have permission to view these recommendations.", "danger")
        return redirect(url_for("dashboard.user_dashboard"))

    recommendations = (
        Recommendation.query.filter_by(resume_id=resume_id)
        .order_by(Recommendation.match_percentage.desc())
        .all()
    )

    flat_skills = resume.get_all_skills_flat()
    nlp_result = nlp_extractor.full_parse(resume.extracted_text or "")
    score_analysis = calculate_resume_completeness(nlp_result, resume.extracted_text or "")

    return render_template(
        "recommendations/results.html",
        resume=resume,
        recommendations=recommendations,
        flat_skills=flat_skills,
        score_analysis=score_analysis
    )


@resume_bp.route("/skill-gap/<int:resume_id>")
@login_required
def view_skill_gap(resume_id: int):
    """Dedicated Skill Gap Analysis view comparing resume against target job role."""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != g.user.user_id and not g.user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("dashboard.user_dashboard"))

    all_jobs = Job.query.order_by(Job.title.asc()).all()
    if not all_jobs:
        flash("No job listings available in the database.", "warning")
        return redirect(url_for("dashboard.user_dashboard"))

    # Selected job ID from query param or default to #1 recommendation
    selected_job_id = request.args.get("job_id", type=int)
    target_job = None
    if selected_job_id:
        target_job = Job.query.get(selected_job_id)

    if not target_job:
        # Default to highest match job for this resume
        top_rec = (
            Recommendation.query.filter_by(resume_id=resume_id)
            .order_by(Recommendation.match_percentage.desc())
            .first()
        )
        if top_rec and top_rec.job:
            target_job = top_rec.job
        else:
            target_job = all_jobs[0]

    candidate_skills = resume.get_all_skills_flat()
    skill_demand = calculate_global_skill_demand()
    gap_data = analyze_skill_gap_for_job(candidate_skills, target_job, skill_demand)

    return render_template(
        "recommendations/skill_gap.html",
        resume=resume,
        all_jobs=all_jobs,
        selected_job=target_job,
        gap_data=gap_data
    )


@resume_bp.route("/resume/delete/<int:resume_id>", methods=["POST"])
@login_required
def delete_resume(resume_id: int):
    """Deletes a resume and its associated recommendation records."""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != g.user.user_id and not g.user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("dashboard.user_dashboard"))

    # Remove physical file if present
    if os.path.exists(resume.file_path):
        try:
            os.remove(resume.file_path)
        except Exception:
            pass

    title = resume.resume_title
    db.session.delete(resume)
    db.session.commit()

    flash(f"Resume '{title}' has been deleted.", "info")
    return redirect(url_for("dashboard.user_dashboard"))
