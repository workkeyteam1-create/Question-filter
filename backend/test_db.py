#!/usr/bin/env python3
"""
Test database initialization
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
import models
from sqlalchemy import inspect

print("Testing database initialization...")
print(f"Database URL: {engine.url}")

try:
    # Try to create tables
    print("\nCreating tables...")
    Base.metadata.create_all(bind=engine)
    print("[SUCCESS] Tables created!")
    
    # Check what tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\nTables in database: {tables}")
    
    # Try a simple query
    from sqlalchemy.orm import Session
    from sqlalchemy import text
    
    with Session(engine) as session:
        # Test connection
        result = session.execute(text("SELECT 1"))
        print(f"[SUCCESS] Database connection test: {result.scalar()}")
        
        # Count tables
        result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = result.fetchall()
        print(f"Tables found: {[table[0] for table in tables]}")
        
    print("\n[SUCCESS] Database is working correctly!")
    
except Exception as e:
    print(f"\n[ERROR] Database test failed: {e}")
    import traceback
    traceback.print_exc()