import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.services.flutterwave import FlutterwaveClient


class PaymentService:
    @staticmethod
    def initialize_order_payment(
        order_id: int,
        current_user,
        db: Session,
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

        if order.status == "paid":
            raise HTTPException(
                status_code=400,
                detail="Order already paid",
            )

        # Generate unique tx_ref
        tx_ref = str(uuid.uuid4())

        flutterwave_response = (
            FlutterwaveClient.initiate_payment(
                email=current_user.email,
                amount=order.total_price,
                tx_ref=tx_ref,
            )
        )

        # Save tx_ref to order
        order.transaction_ref = tx_ref

        db.commit()
        db.refresh(order)

        return {
            "payment_link": (
                flutterwave_response["data"]["link"]
            ),
            "tx_ref": tx_ref,
        }

    @staticmethod
    def verify_order_payment(
        transaction_id: str,
        tx_ref: str,
        db: Session,
    ):
        # Find order using tx_ref
        order = (
            db.query(Order)
            .filter(Order.transaction_ref == tx_ref)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found",
            )

        verification = (
            FlutterwaveClient.verify_payment(
                transaction_id
            )
        )

        payment_data = verification["data"]

        # Validate payment status
        if payment_data["status"] != "successful":
            raise HTTPException(
                status_code=400,
                detail="Payment not successful",
            )

        # Validate tx_ref matches
        if payment_data["tx_ref"] != tx_ref:
            raise HTTPException(
                status_code=400,
                detail="Transaction reference mismatch",
            )

        # Validate amount
        if float(payment_data["amount"]) != float(
            order.total_price
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid payment amount",
            )

        # Prevent duplicate payment updates
        if order.status == "paid":
            return {
                "message": "Order already paid",
                "order_id": order.id,
            }

        # Update order
        order.status = "paid"

        db.commit()
        db.refresh(order)

        return {
            "message": (
                "Payment verified successfully"
            ),
            "order_id": order.id,
            "payment_status": order.status,
        }