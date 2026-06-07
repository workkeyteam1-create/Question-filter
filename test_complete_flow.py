#!/usr/bin/env python3
"""
Test script for complete PDF upload→processing→results flow
"""

import os
import sys
import requests
import time

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:8001"
    
    print("[TEST] Testing complete flow...")
    
    # 1. Test root endpoint
    print("[1] Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"[SUCCESS] Root endpoint: {response.json()}")
        else:
            print(f"[ERROR] Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Root endpoint error: {e}")
        return False
    
    # 2. Test status endpoint
    print("[2] Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/status/")
        if response.status_code == 200:
            status = response.json()
            print(f"[SUCCESS] Status: {status}")
        else:
            print(f"[ERROR] Status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Status endpoint error: {e}")
        return False
    
    # 3. Test upload endpoint with test file
    print("[3] Testing upload endpoint...")
    test_file_path = os.path.join(os.path.dirname(__file__), "test_upload.txt")
    
    if not os.path.exists(test_file_path):
        print(f"[ERROR] Test file not found: {test_file_path}")
        # Create a simple test file
        with open(test_file_path, "w") as f:
            f.write("Test question 1: What is AI?\n")
            f.write("Test question 2: What is machine learning?\n")
        print(f"[INFO] Created test file: {test_file_path}")
    
    try:
        with open(test_file_path, "rb") as f:
            files = [("files", ("test_upload.txt", f, "text/plain"))]
            response = requests.post(f"{base_url}/upload/", files=files)
        
        if response.status_code == 200:
            upload_result = response.json()
            print(f"[SUCCESS] Upload: {upload_result['message']}")
            
            # Get the uploaded file ID
            if upload_result.get("files") and len(upload_result["files"]) > 0:
                file_id = upload_result["files"][0]["id"]
                print(f"[INFO] Uploaded file ID: {file_id}")
                
                # 4. Test process endpoint
                print("[4] Testing process endpoint...")
                time.sleep(1)  # Small delay
                
                response = requests.post(f"{base_url}/process/{file_id}")
                if response.status_code == 200:
                    process_result = response.json()
                    print(f"[SUCCESS] Process: {process_result}")
                    
                    # 5. Test questions endpoint
                    print("[5] Testing questions endpoint...")
                    time.sleep(1)  # Small delay
                    
                    response = requests.get(f"{base_url}/questions/")
                    if response.status_code == 200:
                        questions = response.json()
                        print(f"[SUCCESS] Questions count: {len(questions)}")
                        
                        # 6. Test units endpoint
                        print("[6] Testing units endpoint...")
                        response = requests.get(f"{base_url}/units/")
                        if response.status_code == 200:
                            units = response.json()
                            print(f"[SUCCESS] Units: {units}")
                            
                            # 7. Test sources endpoint
                            print("[7] Testing sources endpoint...")
                            response = requests.get(f"{base_url}/sources/")
                            if response.status_code == 200:
                                sources = response.json()
                                print(f"[SUCCESS] Sources: {sources}")
                                
                                # 8. Test CSV export
                                print("[8] Testing CSV export...")
                                response = requests.get(f"{base_url}/export/csv/")
                                if response.status_code == 200:
                                    print(f"[SUCCESS] CSV export: {len(response.content)} bytes")
                                    
                                    # 9. Test PDF export
                                    print("[9] Testing PDF export...")
                                    response = requests.get(f"{base_url}/export/pdf/")
                                    if response.status_code == 200:
                                        print(f"[SUCCESS] PDF export: {len(response.content)} bytes")
                                        return True
                                    else:
                                        print(f"[ERROR] PDF export failed: {response.status_code}")
                                else:
                                    print(f"[ERROR] CSV export failed: {response.status_code}")
                            else:
                                print(f"[ERROR] Sources endpoint failed: {response.status_code}")
                        else:
                            print(f"[ERROR] Units endpoint failed: {response.status_code}")
                    else:
                        print(f"[ERROR] Questions endpoint failed: {response.status_code}")
                else:
                    print(f"[ERROR] Process endpoint failed: {response.status_code}")
            else:
                print("[ERROR] No files in upload response")
        else:
            print(f"[ERROR] Upload failed: {response.status_code}")
            print(f"[ERROR] Response: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Upload test error: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    print("[INFO] Starting complete flow test...")
    print("[INFO] Make sure backend server is running on port 8001")
    print("[INFO] Backend URL: http://localhost:8001")
    
    success = test_api_endpoints()
    
    if success:
        print("\n" + "="*60)
        print("[SUCCESS] Complete flow test PASSED!")
        print("="*60)
        print("\nAll endpoints tested successfully:")
        print("1. Root endpoint ✓")
        print("2. Status endpoint ✓")
        print("3. Upload endpoint ✓")
        print("4. Process endpoint ✓")
        print("5. Questions endpoint ✓")
        print("6. Units endpoint ✓")
        print("7. Sources endpoint ✓")
        print("8. CSV export ✓")
        print("9. PDF export ✓")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("[FAIL] Complete flow test FAILED!")
        print("="*60)
        sys.exit(1)