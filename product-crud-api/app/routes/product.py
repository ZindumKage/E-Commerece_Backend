from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.crud.product import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
)
from app.auth.dependencies import (
    get_current_user,
    admin_required
)

router = APIRouter(prefix="/products", tags=["Products"]) 


@router.post("/", response_model=ProductResponse)
def create(product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return create_product(db, product)


@router.get("/", response_model=list[ProductResponse])
def get_all(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_one(product_id: int, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    updated = update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not updated")
    return updated

@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    deleted = delete_product(db, product_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not deleted")
    return {"message":"Product deleted successfully"}

