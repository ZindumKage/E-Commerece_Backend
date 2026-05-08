from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

# CRUD operations for Create Product 
def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

# CRUD operation for Get all Products
def get_products(db: Session):
    return db.query(Product).all()

# CRUD operation for Get Product by ID
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# CRUD operation for Update Product
def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product(db, product_id)

    if not db_product:
        return None
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product

# CRUD operation for Delete Product
def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)

    if not db_product:
        return None

    db.delete(db_product)
    db.commit()

    return db_product

