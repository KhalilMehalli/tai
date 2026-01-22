"""
Database configuration and session management.

This module sets up the SQLAlchemy engine and provides the database
session dependency for FastAPI endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# Create the SQLAlchemy engine to communicate with PostgreSQL
engine = create_engine(settings.DB_URL)

# Each API request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models (tables)
# SQLAlchemy uses this to track which classes correspond to database tables
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db # The function will pause here until the seesion will be done
    finally:
        db.close()