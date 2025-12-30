"""
ORM models for the Product CRUD API.
"""

from __future__ import annotations

from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.api.database import Base


class Product(Base):
    """SQLAlchemy ORM model representing a product."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
