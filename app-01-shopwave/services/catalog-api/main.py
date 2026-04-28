"""
catalog-api — returns the list of products as JSON.
A simple FastAPI service used to learn DevOps. The Python here is intentionally tiny.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="catalog-api", version="1.0.0")

# Pretend database -- a hardcoded list of products.
# In real life, this would query Postgres. Today, simplicity wins.
PRODUCTS = [
    {"id": 1, "name": "iPhone 16 Pro Max", "price": 79900, "category": "phones"},
    {"id": 2, "name": "Samsung Galaxy S24", "price": 74999, "category": "phones"},
    {"id": 3, "name": "MacBook Air M3", "price": 114900, "category": "laptops"},
    {"id": 4, "name": "Sony WH-1000XM5", "price": 26990, "category": "audio"},
    {"id": 5, "name": "iPad Pro 13", "price": 99900, "category": "tablets"},
]


@app.get("/")
def root():
    """Friendly landing page so people know they hit the right service."""
    return {"service": "catalog-api", "status": "ok", "version": "1.0.0"}


@app.get("/health")
def health():
    """Health check endpoint -- Kubernetes will hit this every few seconds."""
    return {"status": "healthy"}


@app.get("/products")
def list_products():
    """Return all products."""
    return {"count": len(PRODUCTS), "products": PRODUCTS}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Return one product by id, or 404 if missing."""
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return JSONResponse(status_code=404, content={"error": "product not found"})
