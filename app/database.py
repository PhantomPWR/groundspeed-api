"""
Database connection configuration and session management.
"""

from sqlalchemy import create_engine                     # Third Party: DB engine
from sqlalchemy.ext.declarative import declarative_base  # Third Party: Models
from sqlalchemy.orm import sessionmaker                  # Third Party: Session tool

# Connection string for the SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./groundspeed.db"

# Create the engine (check_same_thread is required for SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


def get_db():
    """
    Dependency function that yields a new database session for each 
    request and ensures it is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
