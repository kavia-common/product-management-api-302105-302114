"""
FastAPI entrypoint for the Product CRUD backend.

Provides:
- Health check endpoint: GET /
- Product CRUD endpoints under /products
- SQLite persistence via SQLAlchemy (local file DB)

Run notes:
- No environment variables are required.
- The SQLite database file will be created automatically (products.db).
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.database import Base, engine
from src.api.routers.products import router as products_router

openapi_tags = [
    {"name": "health", "description": "Basic service health endpoints."},
    {"name": "products", "description": "CRUD operations for products (id, name, price)."},
]

app = FastAPI(
    title="Product CRUD API",
    description="A simple FastAPI backend providing CRUD operations for products using SQLite + SQLAlchemy.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

# Allow common localhost origins for local dev.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Create DB tables if they don't exist (migration-safe create).

    Note: For real migrations, Alembic would be recommended, but this satisfies
    the requirement for safe initialization without destructive operations.
    """
    Base.metadata.create_all(bind=engine)


@app.get(
    "/",
    tags=["health"],
    summary="Health check",
    description="Simple endpoint to verify the service is running.",
    operation_id="health_check",
)
def health_check():
    """Return a minimal health response."""
    return {"message": "Healthy"}


app.include_router(products_router)
