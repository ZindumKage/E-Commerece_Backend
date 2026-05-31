from fastapi import APIRouter

from app.controllers.product import (
    create,
    get_all,
    get_one,
    update,
    delete,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

router.post("/")(create)
router.get("/")(get_all)
router.get("/{product_id}")(get_one)
router.put("/{product_id}")(update)
router.delete("/{product_id}")(delete)