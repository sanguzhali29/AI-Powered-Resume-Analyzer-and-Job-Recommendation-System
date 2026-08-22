"""
AI-Powered Resume Analyzer and Job Recommendation System
========================================================
Main Flask Application Entry Point (Final Year B.E. CSE Project)
Run with: python app.py
"""

import os
from flask import Flask, render_template, redirect, url_for, g
from config import config
from database.connection import db, init_db
from database.seed_data import seed_database
from routes import register_routes
from models.job import Job
from models.skill import Skill
from models.resume import Resume

def create_app(config_name="default"):
    """
    Application factory creating and configuring the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure upload directory exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize Database & Fallback
    init_db(app)

    # Register Blueprints
    register_routes(app)

    # -------------------------------------------------------------
    # Custom Jinja2 Template Filters
    # -------------------------------------------------------------
    @app.template_filter("badge_color")
    def badge_color(category):
        """Returns appropriate Bootstrap badge color based on skill category."""
        mapping = {
            "programming_languages": "primary",
            "frameworks": "success",
            "databases": "info",
            "tools": "warning text-dark",
            "domain": "purple",
            "soft_skills": "secondary"
        }
        return mapping.get(category, "primary")

    @app.template_filter("score_badge")
    def score_badge(score):
        """Returns badge class and label based on match percentage."""
        score = float(score) if score else 0.0
        if score >= 75:
            return "bg-success text-white"
        elif score >= 50:
            return "bg-primary text-white"
        elif score >= 30:
            return "bg-warning text-dark"
        else:
            return "bg-danger text-white"

    # -------------------------------------------------------------
    # Global Landing Route
    # -------------------------------------------------------------
    @app.route("/")
    def index():
        """Public landing page displaying overview, metrics, and how it works."""
        if hasattr(g, "user") and g.user:
            if g.user.is_admin:
                return redirect(url_for("dashboard.admin_dashboard"))
            return redirect(url_for("dashboard.user_dashboard"))

        total_jobs = Job.query.count()
        total_skills = Skill.query.count()
        total_resumes = Resume.query.count()
        sample_jobs = Job.query.order_by(Job.job_id.asc()).limit(6).all()

        return render_template(
            "index.html",
            total_jobs=total_jobs,
            total_skills=total_skills,
            total_resumes=total_resumes,
            sample_jobs=sample_jobs
        )

    # -------------------------------------------------------------
    # Error Handlers
    # -------------------------------------------------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("base.html", error_title="404 - Page Not Found", error_msg="The requested page could not be located."), 404

    @app.errorhandler(413)
    def file_too_large(e):
        return render_template("base.html", error_title="413 - File Too Large", error_msg="Uploaded resume exceeds maximum allowed size (16 MB)."), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("base.html", error_title="500 - Internal Server Error", error_msg="An unexpected error occurred while processing your request."), 500

    # -------------------------------------------------------------
    # CLI Commands
    # -------------------------------------------------------------
    @app.cli.command("seed")
    def seed_cmd():
        """Command to manually seed initial skills and job descriptions."""
        with app.app_context():
            seed_database()
            print("Seeding finished.")

    # Auto-seed database if empty on startup
    with app.app_context():
        try:
            if Job.query.count() == 0:
                print("[Startup] Empty database detected. Auto-seeding initial master data...")
                seed_database()
        except Exception as e:
            print(f"[Startup Note] {e}")

    return app


# Create default Flask app instance
app = create_app(os.environ.get("FLASK_ENV", "default"))


if __name__ == "__main__":
    print("=" * 70)
    print(" AI-Powered Resume Analyzer & Job Recommendation System")
    print(" Final Year B.E. Computer Science & Engineering Project")
    print("=" * 70)
    print(" -> Server starting on: http://127.0.0.1:5000")
    print(" -> Demo Student: student@demo.com | password123")
    print(" -> Demo Admin:   admin@demo.com   | admin123")
    print("=" * 70)
    app.run(debug=True, host="127.0.0.1", port=5000)