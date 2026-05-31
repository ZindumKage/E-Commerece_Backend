from sqlalchemy.orm import Session

from app.schemas.order import OrderCreate
from app.services.order import OrderService


class OrderController:
    @staticmethod
    def create_order(
        payload: OrderCreate,
        current_user,
        db: Session,
    ):
        return OrderService.create_order(db, payload, current_user)
    
    @staticmethod
    def get_user_orders(
        current_user,
        db: Session,
    ):
        return OrderService.get_user_orders(db, current_user)
    
    @staticmethod
    def get_single_order(
        db: Session,
        order_id: int,
        current_user,
    ):
        return OrderService.get_single_order(db, order_id, current_user)