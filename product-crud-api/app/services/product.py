from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.product import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
)

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)


def create_product_service(
    db: Session,
    product: ProductCreate,
):
    return create_product(db, product)


def get_products_service(db: Session):
    return get_products(db)


def get_product_service(
    db: Session,
    product_id: int,
):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


def update_product_service(
    db: Session,
    product_id: int,
    product: ProductUpdate,
):
    updated = update_product(
        db,
        product_id,
        product,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Product not updated",
        )

    return updated


def delete_product_service(
    db: Session,
    product_id: int,
):
    deleted = delete_product(db, product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not deleted",
        )

    return {
        "message": "Product deleted successfully"
    }