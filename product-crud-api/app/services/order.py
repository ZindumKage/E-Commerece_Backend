from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate


class OrderService:

    @staticmethod
    def create_order(
        db: Session,
        payload: OrderCreate,
        current_user,
    ):

        total_price = 0

        order = Order(
            user_id=current_user.id,
            total_price=0,
            status="pending",
        )

        db.add(order)
        db.flush()

        for item in payload.items:

            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .first()
            )

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {item.product_id} not found",
                )

            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {product.name}",
                )

            item_total = product.price * item.quantity
            total_price += item_total

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price,
            )

            db.add(order_item)

            # optional stock reduction
            product.stock_quantity -= item.quantity

        order.total_price = total_price

        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def get_user_orders(
        db: Session,
        current_user,
    ):
        return (
            db.query(Order)
            .filter(Order.user_id == current_user.id)
            .all()
        )

    @staticmethod
    def get_single_order(
        db: Session,
        order_id: int,
        current_user,
    ):

        order = (
            db.query(Order)
            .filter(
                Order.id == order_id,
                Order.user_id == current_user.id,
            )
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found",
            )

        return order