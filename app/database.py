"""
Database connection configuration with naming conventions for migrations.
"""

from sqlalchemy import create_engine, MetaData    # Added MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define a naming convention for SQLite constraints
# This prevents the "Constraint must have a name" error in Alembic
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

SQLALCHEMY_DATABASE_URL = "sqlite:///./groundspeed.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Pass the convention to the Base class
Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))


def get_db():
    """Dependency for DB session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
