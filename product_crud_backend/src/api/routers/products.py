"""
Product CRUD routes.

Endpoints:
- GET /products: List products
- POST /products: Create a product
- GET /products/{id}: Read a single product
- PUT /products/{id}: Update a product
- DELETE /products/{id}: Delete a product
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api import models, schemas
from src.api.database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "",
    response_model=List[schemas.ProductRead],
    summary="List products",
    description="Return all products in the database.",
    operation_id="list_products",
)
def list_products(db: Session = Depends(get_db)) -> List[schemas.ProductRead]:
    """List all products."""
    return db.query(models.Product).order_by(models.Product.id.asc()).all()


@router.post(
    "",
    response_model=schemas.ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="Create a new product with a name and price.",
    operation_id="create_product",
)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)) -> schemas.ProductRead:
    """Create a new product."""
    product = models.Product(name=payload.name, price=payload.price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get(
    "/{id}",
    response_model=schemas.ProductRead,
    summary="Get product",
    description="Fetch a single product by its ID.",
    operation_id="get_product",
)
def get_product(id: int, db: Session = Depends(get_db)) -> schemas.ProductRead:
    """Get a product by ID."""
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.put(
    "/{id}",
    response_model=schemas.ProductRead,
    summary="Update product",
    description="Update an existing product by ID.",
    operation_id="update_product",
)
def update_product(id: int, payload: schemas.ProductUpdate, db: Session = Depends(get_db)) -> schemas.ProductRead:
    """Update an existing product by ID."""
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product.name = payload.name
    product.price = payload.price

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Delete an existing product by ID.",
    operation_id="delete_product",
)
def delete_product(id: int, db: Session = Depends(get_db)) -> None:
    """Delete a product by ID."""
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()
    return None
