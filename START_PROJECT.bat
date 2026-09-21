@echo off
title AI Resume Analyzer Launcher
color 0b
echo ======================================================================
echo   AI-POWERED RESUME ANALYZER & JOB RECOMMENDATION SYSTEM
echo   Launching Application & Opening Browser Automatically...
echo ======================================================================
echo.

cd /d "%~dp0"

if exist "venv\Scripts\python.exe" (
    echo [OK] Virtual environment found.
    echo [OK] Starting Server and Opening Browser...
    echo.
    echo Demo Student Login: student@demo.com ^| password123
    echo Demo Admin Login:   admin@demo.com   ^| admin123
    echo.
    echo Press Ctrl+C in this window when you want to stop the server.
    echo.
    "venv\Scripts\python.exe" run.py
) else (
    echo [!] Virtual environment not found. Using system python...
    python run.py
)

pause
