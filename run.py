"""
1-Click Desktop Launcher for AI-Powered Resume Analyzer
======================================================
Automatically launches the Flask server and opens your default browser.
Just double-click START_PROJECT.bat to run!
"""

import os
import sys
import time
import webbrowser
import threading
from app import app

def open_browser():
    """Wait 1.5 seconds for the server to bind, then open the browser."""
    time.sleep(1.5)
    url = "http://127.0.0.1:5000"
    print(f"[Launcher] Opening browser at {url} ...")
    webbrowser.open(url)

if __name__ == "__main__":
    print("=" * 70)
    print(" AI-Powered Resume Analyzer & Job Recommendation System")
    print(" 1-Click Launcher: Server is starting and opening in your browser...")
    print("=" * 70)
    
    # Start browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask Web Server
    app.run(debug=False, host="127.0.0.1", port=5000)
