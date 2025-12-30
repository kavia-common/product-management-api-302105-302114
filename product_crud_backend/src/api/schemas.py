"""
Pydantic schemas for the Product CRUD API.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    """Shared properties for Product create/update schemas."""

    name: str = Field(..., min_length=1, max_length=255, description="Name of the product")
    price: float = Field(..., ge=0, description="Price of the product (must be >= 0)")


class ProductCreate(ProductBase):
    """Schema for product creation payload."""


class ProductUpdate(ProductBase):
    """Schema for product update payload."""


class ProductRead(ProductBase):
    """Schema returned by API for product objects."""

    id: int = Field(..., description="Product ID")

    model_config = ConfigDict(from_attributes=True)
