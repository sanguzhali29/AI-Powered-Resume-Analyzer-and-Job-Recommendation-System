"""
Authentication & Authorization Routes (Phase 3)
==============================================
Handles user registration, login, logout, 1-click quick demo access,
session management, and access control decorators.
"""

from functools import wraps
from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, flash, session, g
)
from database.connection import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


def login_required(f):
    """Decorator to require user login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in or use 1-Click Demo Login to continue.", "info")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role for privileged routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in with an administrator account.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        if session.get("user_role") != "admin":
            flash("Access denied. Administrator privileges required.", "danger")
            return redirect(url_for("dashboard.user_dashboard"))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.before_app_request
def load_logged_in_user():
    """Loads currently logged-in user into Flask's `g` context."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handles new student/candidate registration."""
    if g.user:
        return redirect(url_for("dashboard.user_dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        phone = request.form.get("phone", "").strip()

        # Validation checks
        if not full_name or not email or not password:
            flash("Full Name, Email, and Password are required.", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("auth/register.html")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email address already exists. Please log in.", "warning")
            return redirect(url_for("auth.login"))

        # Create new student user
        new_user = User(
            full_name=full_name,
            email=email,
            role="student",
            phone=phone if phone else None
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Auto-login after registration
        session.clear()
        session["user_id"] = new_user.user_id
        session["user_name"] = new_user.full_name
        session["user_email"] = new_user.email
        session["user_role"] = new_user.role
        session.permanent = True

        flash(f"Welcome, {new_user.full_name}! Registration successful.", "success")
        return redirect(url_for("resume.upload_resume"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handles user and administrator authentication."""
    if g.user:
        if g.user.is_admin:
            return redirect(url_for("dashboard.admin_dashboard"))
        return redirect(url_for("dashboard.user_dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.user_id
            session["user_name"] = user.full_name
            session["user_email"] = user.email
            session["user_role"] = user.role
            session.permanent = True  # Always remember for 90 days

            flash(f"Welcome back, {user.full_name}!", "success")
            
            # Redirect to next URL or appropriate dashboard
            next_page = request.args.get("next")
            if next_page and not next_page.startswith("//"):
                return redirect(next_page)

            if user.is_admin:
                return redirect(url_for("dashboard.admin_dashboard"))
            return redirect(url_for("dashboard.user_dashboard"))
        else:
            flash("Invalid email or password. You can also use the 1-Click Instant Login buttons below!", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/quick-login/student")
def quick_student_login():
    """1-Click Instant Login as Student (No password typing needed)."""
    user = User.query.filter_by(email="student@demo.com").first()
    if not user:
        # Fallback to first student or create one
        user = User.query.filter_by(role="student").first()
    if not user:
        user = User(full_name="Aravind Kumar", email="student@demo.com", role="student")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    session.clear()
    session["user_id"] = user.user_id
    session["user_name"] = user.full_name
    session["user_email"] = user.email
    session["user_role"] = user.role
    session.permanent = True

    flash("Logged in successfully as Demo Student! (1-Click Instant Access)", "success")
    return redirect(url_for("resume.upload_resume"))


@auth_bp.route("/quick-login/admin")
def quick_admin_login():
    """1-Click Instant Login as Admin (No password typing needed)."""
    user = User.query.filter_by(email="admin@demo.com").first()
    if not user:
        user = User.query.filter_by(role="admin").first()
    if not user:
        user = User(full_name="System Administrator", email="admin@demo.com", role="admin")
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()

    session.clear()
    session["user_id"] = user.user_id
    session["user_name"] = user.full_name
    session["user_email"] = user.email
    session["user_role"] = user.role
    session.permanent = True

    flash("Logged in successfully as Administrator!", "success")
    return redirect(url_for("dashboard.admin_dashboard"))


@auth_bp.route("/logout")
def logout():
    """Logs the user out and clears session state."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
