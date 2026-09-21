"""
Authentication & Authorization Routes (Phase 3)
==============================================
Handles user registration, login, logout, session management,
and access control decorators.
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
            flash("Please log in to access this page.", "warning")
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

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

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
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.user_id
            session["user_name"] = user.full_name
            session["user_email"] = user.email
            session["user_role"] = user.role
            session.permanent = remember

            flash(f"Welcome back, {user.full_name}!", "success")
            
            # Redirect to next URL or appropriate dashboard
            next_page = request.args.get("next")
            if next_page and not next_page.startswith("//"):
                return redirect(next_page)

            if user.is_admin:
                return redirect(url_for("dashboard.admin_dashboard"))
            return redirect(url_for("dashboard.user_dashboard"))
        else:
            flash("Invalid email or password. Please check your credentials.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    """Logs the user out and clears session state."""
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("auth.login"))
