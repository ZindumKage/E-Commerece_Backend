from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.controllers.payment import PaymentController
from app.database import get_db


router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/initialize/{order_id}")
def initialize_payment(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return PaymentController.initialize_payment(
        order_id,
        current_user,
        db
    )
    
@router.get("/verify/{tx_ref}")
def verify_payment(
    tx_ref: str,
    transaction_id: str,
    db: Session = Depends(get_db),
):
    return PaymentController.verify_payment(
        tx_ref,
        transaction_id,
        db
    )