from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

# SQLite database URL - create in the backend directory
db_path = os.path.join(os.path.dirname(__file__), "question_filter.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

print(f"[INFO] Database path: {db_path}")

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models - imported by models.py
Base = declarative_base()