#!/usr/bin/env python3
"""
Test script for Question Filter System
This script tests the basic functionality of the system
"""

import os
import sys
import tempfile
from pathlib import Path

def test_backend_structure():
    """Test if backend files exist"""
    print("Testing backend structure...")
    
    backend_files = [
        "backend/main.py",
        "backend/database.py", 
        "backend/models.py",
        "backend/schemas.py",
        "backend/services.py",
        "backend/requirements.txt"
    ]
    
    all_exist = True
    for file_path in backend_files:
        full_path = Path(file_path)
        if full_path.exists():
            print(f"  [OK] {file_path}")
        else:
            print(f"  [FAIL] {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_frontend_structure():
    """Test if frontend files exist"""
    print("\nTesting frontend structure...")
    
    frontend_files = [
        "frontend/index.html"
    ]
    
    all_exist = True
    for file_path in frontend_files:
        full_path = Path(file_path)
        if full_path.exists():
            print(f"  [OK] {file_path}")
        else:
            print(f"  [FAIL] {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    
    directories = [
        "uploads"
    ]
    
    all_exist = True
    for dir_path in directories:
        full_path = Path(dir_path)
        if full_path.exists() and full_path.is_dir():
            print(f"  [OK] {dir_path}/")
        else:
            print(f"  [FAIL] {dir_path}/ - MISSING")
            all_exist = False
    
    return all_exist

def test_python_dependencies():
    """Test if Python dependencies can be imported"""
    print("\nTesting Python dependencies...")
    
    # Change to backend directory
    original_dir = os.getcwd()
    backend_dir = Path("backend")
    
    if backend_dir.exists():
        os.chdir(backend_dir)
    
    dependencies = [
        "fastapi",
        "sqlalchemy",
        "pydantic",
        "pdfplumber",
        "pypdf2",
        "pandas",
        "reportlab"
    ]
    
    all_imported = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  [OK] {dep}")
        except ImportError as e:
            print(f"  [FAIL] {dep} - {e}")
            all_imported = False
    
    # Change back to original directory
    os.chdir(original_dir)
    
    return all_imported

def create_sample_pdf():
    """Create a sample PDF for testing"""
    print("\nCreating sample PDF for testing...")
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        # Create temp PDF file
        temp_dir = Path("uploads")
        temp_dir.mkdir(exist_ok=True)
        
        pdf_path = temp_dir / "sample_test.pdf"
        
        # Create PDF with sample questions
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.setFont("Helvetica", 12)
        
        # Add title
        c.drawString(100, 750, "Sample Questions for Testing")
        c.drawString(100, 730, "=================================")
        
        # Add questions
        questions = [
            "Q1. What is a perceptron and how does it work?",
            "Q2. Explain the backpropagation algorithm in neural networks.",
            "Q3. How does gradient descent optimize model parameters?",
            "Q4. Describe the XOR problem and its significance.",
            "Q5. What are activation functions in neural networks?",
            "Q6. Explain the difference between supervised and unsupervised learning.",
            "Q7. How do convolutional neural networks process images?",
            "Q8. What is the purpose of pooling layers in CNNs?",
            "Q9. Describe recurrent neural networks and their applications.",
            "Q10. What is the vanishing gradient problem in deep learning?"
        ]
        
        y_position = 700
        for i, question in enumerate(questions):
            c.drawString(100, y_position, question)
            y_position -= 25
            
            if i == 4:  # Start new page after 5 questions
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = 750
        
        c.save()
        
        print(f"  [OK] Created sample PDF: {pdf_path}")
        print(f"  [OK] File size: {pdf_path.stat().st_size} bytes")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Failed to create sample PDF: {e}")
        return False

def test_system_flow():
    """Test the complete system flow"""
    print("\n" + "="*60)
    print("SYSTEM TEST SUMMARY")
    print("="*60)
    
    tests = [
        ("Backend Structure", test_backend_structure()),
        ("Frontend Structure", test_frontend_structure()),
        ("Directories", test_directories()),
        ("Python Dependencies", test_python_dependencies()),
        ("Sample PDF Creation", create_sample_pdf())
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:25} : {status}")
        if result:
            passed += 1
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] SYSTEM READY FOR USE!")
        print("\nNext steps:")
        print("1. cd 'Question Filter App/backend'")
        print("2. pip install -r requirements.txt")
        print("3. python main.py")
        print("4. Open frontend/index.html in your browser")
        print("5. Upload the sample_test.pdf from uploads/ folder")
    else:
        print("\n[WARNING] Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    # Change to the project directory
    project_dir = Path("Question Filter App")
    if project_dir.exists():
        os.chdir(project_dir)
    
    success = test_system_flow()
    sys.exit(0 if success else 1)