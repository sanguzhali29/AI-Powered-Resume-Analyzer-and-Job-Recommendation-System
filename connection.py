"""
Database Connection & Session Factory
=====================================
Initializes SQLAlchemy ORM object and provides database setup helpers.
Supports automatic fallback to SQLite when MySQL is unreachable.
"""

import logging
import pymysql
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy ORM instance
db = SQLAlchemy()

def init_db(app):
    """
    Initializes the database with the Flask application context.
    Checks if MySQL is reachable; if not, automatically reconfigures to SQLite fallback
    before initializing SQLAlchemy, ensuring 100% zero-friction execution.
    """
    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    
    if database_uri.startswith("mysql"):
        try:
            # Quick ping to check if MySQL daemon is running locally
            user = app.config.get("DB_USER", "root")
            password = app.config.get("DB_PASSWORD", "password")
            host = app.config.get("DB_HOST", "localhost")
            port = int(app.config.get("DB_PORT", 3306))
            
            conn = pymysql.connect(
                host=host, 
                user=user, 
                password=password, 
                port=port, 
                connect_timeout=1
            )
            conn.close()
            logging.info("[DB] Connected successfully to MySQL database.")
        except Exception as e:
            logging.warning(
                f"[DB Note] MySQL service not active on localhost:3306 ({e}). "
                f"Using local SQLite database fallback for instant execution."
            )
            app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("SQLITE_URI")
            # Clear engine options specific to MySQL
            app.config.pop("SQLALCHEMY_ENGINE_OPTIONS", None)

    db.init_app(app)
    
    with app.app_context():
        db.create_all()
