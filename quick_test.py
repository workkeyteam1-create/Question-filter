#!/usr/bin/env python3
"""
Quick test script to verify the Question Filter System is working
"""

import requests
import json
import os
from pathlib import Path

def test_api_connection():
    """Test if the API is responding"""
    print("Testing API connection...")
    
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("[SUCCESS] API is running!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"[ERROR] API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to API. Is the server running?")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def test_database_file():
    """Check if database file exists"""
    print("\nChecking database file...")
    
    db_path = Path("question_filter.db")
    if db_path.exists():
        print(f"[SUCCESS] Database file exists: {db_path}")
        print(f"Size: {db_path.stat().st_size} bytes")
        return True
    else:
        print(f"[WARNING] Database file not found: {db_path}")
        
        # Check in backend directory
        backend_db = Path("backend/question_filter.db")
        if backend_db.exists():
            print(f"[SUCCESS] Database file found in backend directory: {backend_db}")
            return True
        else:
            print("[ERROR] Database file not found in any expected location")
            return False

def test_upload_endpoint():
    """Test the upload endpoint"""
    print("\nTesting upload endpoint...")
    
    # Create a simple test file
    test_file = "test_upload.txt"
    with open(test_file, "w") as f:
        f.write("This is a test file for upload testing.")
    
    try:
        files = {'files': open(test_file, 'rb')}
        response = requests.post("http://localhost:8001/upload/", files=files)
        
        if response.status_code == 200:
            print("[SUCCESS] Upload endpoint is working!")
            print(f"Response: {response.json()}")
            
            # Clean up test file
            os.remove(test_file)
            return True
        else:
            print(f"[ERROR] Upload failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Clean up test file
            os.remove(test_file)
            return False
            
    except Exception as e:
        print(f"[ERROR] Upload test failed: {e}")
        
        # Clean up test file if it exists
        if os.path.exists(test_file):
            os.remove(test_file)
        return False

def test_questions_endpoint():
    """Test the questions endpoint"""
    print("\nTesting questions endpoint...")
    
    try:
        response = requests.get("http://localhost:8001/questions/", timeout=5)
        
        if response.status_code == 200:
            print("[SUCCESS] Questions endpoint is working!")
            questions = response.json()
            print(f"Number of questions: {len(questions)}")
            
            if len(questions) > 0:
                print("Sample question:")
                print(json.dumps(questions[0], indent=2))
            
            return True
        else:
            print(f"[ERROR] Questions endpoint returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Questions test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Question Filter System - Quick Test")
    print("=" * 60)
    
    # Change to project directory
    project_dir = Path("Question Filter App")
    if project_dir.exists():
        os.chdir(project_dir)
        print(f"Changed to directory: {os.getcwd()}")
    
    tests = [
        ("API Connection", test_api_connection()),
        ("Database File", test_database_file()),
        ("Upload Endpoint", test_upload_endpoint()),
        ("Questions Endpoint", test_questions_endpoint()),
    ]
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} : {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! The system is ready.")
        print("\nAccess the application at: http://localhost:8080")
        print("Backend API: http://localhost:8001")
    else:
        print("\n[WARNING] Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)