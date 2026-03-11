#!/usr/bin/env python3
"""
EDIS Backend Startup Script
"""

import os
import sys
import subprocess

def install_dependencies():
    """Install required Python packages"""
    packages = [
        "fastapi",
        "uvicorn", 
        "requests",
        "pandas",
        "numpy",
        "scikit-learn",
        "joblib",
        "groq",
        "python-dotenv",
        "reportlab"
    ]
    
    print("Installing Python dependencies...")
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def start_server():
    """Start the FastAPI server"""
    print("\nStarting EDIS Backend Server...")
    try:
        # Change to backend directory
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(backend_dir)
        
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

if __name__ == "__main__":
    print("EDIS Backend Setup")
    print("=" * 30)
    
    # Install dependencies
    if install_dependencies():
        print("\n✅ Dependencies installed successfully")
        start_server()
    else:
        print("❌ Failed to install dependencies")
        sys.exit(1)
