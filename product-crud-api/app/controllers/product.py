from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)

from app.services.product import (
    create_product_service,
    get_products_service,
    get_product_service,
    update_product_service,
    delete_product_service,
)

from app.auth.dependencies import (
    get_current_user,
    admin_required,
)


def create(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    return create_product_service(db, product)


def get_all(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_products_service(db)


def get_one(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_product_service(db, product_id)


def update(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    return update_product_service(db, product_id, product)


def delete(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    return delete_product_service(db, product_id)