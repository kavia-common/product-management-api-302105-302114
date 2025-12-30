"""
Database configuration for the Product CRUD API.

This module:
- Creates a SQLite engine using a local file database.
- Exposes SessionLocal for transactional session usage.
- Exposes a dependency provider for FastAPI routes.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Local SQLite file DB. No env vars needed.
SQLALCHEMY_DATABASE_URL = "sqlite:///./products.db"

# check_same_thread=False is required for SQLite when used with FastAPI's threaded concurrency model.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""


# PUBLIC_INTERFACE
def get_db() -> Generator:
    """FastAPI dependency that yields a SQLAlchemy DB session and ensures it is closed.

    Yields:
        sqlalchemy.orm.Session: A database session for the duration of the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
