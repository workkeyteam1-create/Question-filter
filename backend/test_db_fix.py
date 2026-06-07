#!/usr/bin/env python3
"""
Test script to verify database creation works correctly
"""

import os
import sys
from sqlalchemy import inspect

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from database import engine, Base
import models

def test_database_creation():
    """Test if database tables can be created"""
    print("[TEST] Testing database creation...")
    
    # Check if database file exists
    db_path = os.path.join(os.path.dirname(__file__), "question_filter.db")
    print(f"[INFO] Database path: {db_path}")
    print(f"[INFO] Database exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        print(f"[INFO] Database size: {os.path.getsize(db_path)} bytes")
    
    # Try to create tables
    try:
        print("[INFO] Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Tables created successfully!")
        
        # Check what tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"[INFO] Tables in database: {tables}")
        
        # Check if our tables exist
        required_tables = ['uploaded_files', 'questions']
        for table in required_tables:
            if table in tables:
                print(f"[SUCCESS] Table '{table}' exists")
            else:
                print(f"[ERROR] Table '{table}' missing")
                
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to create tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_creation()
    if success:
        print("\n[SUCCESS] Database test passed!")
        sys.exit(0)
    else:
        print("\n[FAIL] Database test failed!")
        sys.exit(1)