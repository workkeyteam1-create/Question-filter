#!/usr/bin/env python3
"""
Database initialization script for Question Filter System
Run this script once to create the database tables
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
import models

def init_database():
    """Initialize the database by creating all tables"""
    print("Initializing database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Database tables created successfully!")
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"[SUCCESS] Tables created: {tables}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating database tables: {e}")
        return False

def check_database():
    """Check if database tables exist"""
    print("Checking database status...")
    
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['uploaded_files', 'questions']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"[ERROR] Missing tables: {missing_tables}")
            return False
        else:
            print(f"[SUCCESS] All required tables exist: {tables}")
            return True
            
    except Exception as e:
        print(f"[ERROR] Error checking database: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Question Filter System - Database Initialization")
    print("=" * 60)
    
    # Check current status
    if check_database():
        print("\nDatabase already initialized.")
        response = input("Do you want to reinitialize? (y/n): ").lower()
        if response != 'y':
            print("Exiting...")
            sys.exit(0)
    
    # Initialize database
    print("\n" + "-" * 60)
    success = init_database()
    
    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] Database initialization complete!")
        print("You can now start the backend server with: python main.py")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("[ERROR] Database initialization failed!")
        print("Please check the error message above.")
        print("=" * 60)
        sys.exit(1)