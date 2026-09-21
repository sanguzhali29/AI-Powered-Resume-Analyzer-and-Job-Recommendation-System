"""
Routes Package Initialization
=============================
Registers all Flask Blueprint modules.
"""

from routes.auth_routes import auth_bp
from routes.resume_routes import resume_bp
from routes.job_routes import job_bp
from routes.dashboard_routes import dashboard_bp
from routes.learning_routes import learning_bp
from routes.api_routes import api_bp

def register_routes(app):
    """Registers all blueprints on the Flask application instance."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(api_bp)
