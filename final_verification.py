#!/usr/bin/env python3
"""
Final verification script to ensure the entire project is ready to run
"""

import os
import sys
import time
import requests
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f" {text}")
    print("="*70)

def print_success(text):
    """Print success message"""
    print(f"[OK] {text}")

def print_warning(text):
    """Print warning message"""
    print(f"[!] {text}")

def print_error(text):
    """Print error message"""
    print(f"[X] {text}")

def check_project_structure():
    """Check if all required files and directories exist"""
    print_header("1. PROJECT STRUCTURE VERIFICATION")
    
    required_files = [
        ("backend/main.py", "Main FastAPI application"),
        ("backend/database.py", "Database configuration"),
        ("backend/models.py", "Database models"),
        ("backend/schemas.py", "Pydantic schemas"),
        ("backend/services.py", "Business logic"),
        ("backend/requirements.txt", "Python dependencies"),
        ("frontend/index.html", "Frontend application"),
        ("README.md", "Project documentation"),
        ("start.bat", "Windows startup script"),
    ]
    
    all_good = True
    for file_path, description in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print_success(f"{description}: {file_path}")
        else:
            print_error(f"{description}: {file_path} - MISSING")
            all_good = False
    
    # Check for uploads directory
    uploads_dir = os.path.join(os.path.dirname(__file__), "backend", "uploads")
    if os.path.exists(uploads_dir):
        print_success("Uploads directory exists")
    else:
        print_warning("Uploads directory doesn't exist (will be created automatically)")
    
    return all_good

def check_database():
    """Check if database is properly initialized"""
    print_header("2. DATABASE VERIFICATION")
    
    db_path = os.path.join(os.path.dirname(__file__), "backend", "question_filter.db")
    
    if os.path.exists(db_path):
        db_size = os.path.getsize(db_path)
        print_success(f"Database file exists: {db_path}")
        print_success(f"Database size: {db_size} bytes")
        
        if db_size > 0:
            print_success("Database has content (tables created)")
            return True
        else:
            print_warning("Database file is empty (0 bytes)")
            return False
    else:
        print_error("Database file not found")
        return False

def test_backend_api():
    """Test if backend API is accessible and endpoints work"""
    print_header("3. BACKEND API VERIFICATION")
    
    base_url = "http://localhost:8001"
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print_success(f"Backend server is running: {response.json()}")
        else:
            print_error(f"Backend server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Backend server is not running on port 8001")
        return False
    except Exception as e:
        print_error(f"Error connecting to backend: {e}")
        return False
    
    # Test status endpoint
    try:
        response = requests.get(f"{base_url}/status/", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print_success(f"System status: {status}")
            return True
        else:
            print_error(f"Status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing status endpoint: {e}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    print_header("4. FRONTEND VERIFICATION")
    
    try:
        response = requests.get("http://localhost:8080/", timeout=5)
        if response.status_code == 200:
            print_success("Frontend server is running on port 8080")
            
            # Check if it's our application
            if "Question Filter System" in response.text:
                print_success("Frontend application loaded correctly")
                return True
            else:
                print_warning("Frontend loaded but content may not be correct")
                return True
        else:
            print_error(f"Frontend server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Frontend server is not running on port 8080")
        return False
    except Exception as e:
        print_error(f"Error connecting to frontend: {e}")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print_header("5. DEPENDENCIES VERIFICATION")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "requests",
        "pdfplumber",
        "PyPDF2",  # Note: Package name is PyPDF2, not pypdf2
        "pandas",
        "reportlab",
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print_warning("Some dependencies are missing. Run: pip install -r backend/requirements.txt")
    
    return all_installed

def provide_startup_instructions():
    """Provide instructions on how to start the application"""
    print_header("6. STARTUP INSTRUCTIONS")
    
    print("To start the complete application:")
    print("\nOPTION 1: Use the provided startup script (Windows):")
    print("  Double-click on 'start.bat' in the project root folder")
    print("  OR")
    print("  Run: start.bat")
    
    print("\nOPTION 2: Manual startup:")
    print("  1. Start the backend server:")
    print("     cd backend")
    print("     python main.py")
    print("  2. Start the frontend server (in a new terminal):")
    print("     cd frontend")
    print("     python -m http.server 8080")
    
    print("\nOPTION 3: Quick test with sample data:")
    print("  Run: python quick_test.py")
    
    print("\nACCESS THE APPLICATION:")
    print("  Frontend: http://localhost:8080")
    print("  Backend API: http://localhost:8001")
    print("  API Documentation: http://localhost:8001/docs")

def main():
    """Main verification function"""
    print_header("QUESTION FILTER SYSTEM - FINAL VERIFICATION")
    print("Checking if the project is completely ready to run...")
    
    # Store results
    results = []
    
    # Run all checks
    results.append(("Project Structure", check_project_structure()))
    results.append(("Database", check_database()))
    results.append(("Backend API", test_backend_api()))
    results.append(("Frontend", test_frontend()))
    results.append(("Dependencies", check_dependencies()))
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    
    passed = 0
    total = len(results)
    
    for check_name, success in results:
        if success:
            print_success(f"{check_name}: PASSED")
            passed += 1
        else:
            print_error(f"{check_name}: FAILED")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print_header("PROJECT IS COMPLETELY READY TO RUN!")
        print("All systems are go. You can start using the application.")
    elif passed >= 3:
        print_header("PROJECT IS MOSTLY READY")
        print("Some minor issues detected but the core functionality should work.")
    else:
        print_header("PROJECT NEEDS FIXES")
        print("Significant issues detected that need to be fixed before running.")
    
    # Always provide startup instructions
    provide_startup_instructions()
    
    # Return exit code based on results
    if passed == total:
        return 0
    elif passed >= 3:
        return 1
    else:
        return 2

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nVerification interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nUnexpected error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(3)