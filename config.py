"""
Configuration Module for AI-Powered Resume Analyzer & Job Recommendation System
================================================================================
Defines configuration classes for development, testing, and production environments.
Supports MySQL database connection with graceful SQLite fallback.
"""

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "final-year-cse-project-secret-key-2026")
    
    # Upload Settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB maximum file size limit
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
    
    # Session Settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Database Configuration (MySQL with fallback)
    # Format: mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_NAME = os.environ.get("DB_NAME", "resume_analyzer_db")
    
    MYSQL_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLITE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'resume_analyzer.db')}"
    
    # Default URI (env var -> MySQL -> SQLite fallback)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", MYSQL_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
        "connect_args": {"connect_timeout": 2}
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


# Active configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
