from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.controllers.order import OrderController
from app.database import get_db
from app.schemas.order import (OrderCreate, OrderResponse)
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"],)

@router.post("/", response_model=OrderResponse)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return OrderController.create_order(
        payload,
        current_user,
        db,
    )
    
@router.get("/my-orders", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return OrderController.get_user_orders(
        current_user,
        db,
    )
    
@router.get("/{order_id}", response_model=OrderResponse)
def get_single_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return OrderController.get_single_order(
        db,
        order_id,
        current_user,
    )