"""Database configuration and session management.

This module handles database connection setup, session management,
and provides utilities for database operations.
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.models import Base

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///instance/app.db"
)  # Default to SQLite in instance folder

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize the database by creating all tables.

    This function creates all tables defined in the models if they
    don't already exist.
    """
    # Ensure instance directory exists
    instance_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", ""))
    if instance_dir and not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    # Create all tables
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for dependency injection.

    Yields:
        Session: A SQLAlchemy database session

    Note:
        This function ensures that database sessions are properly
        closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 