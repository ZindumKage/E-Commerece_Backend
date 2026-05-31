from sqlalchemy.orm import Session

from app.services.payment import PaymentService


class PaymentController:
    @staticmethod
    def initialize_payment(
        order_id: int,
        current_user,
        db: Session,
    ):
        return PaymentService.initialize_order_payment(
            order_id,
            current_user,
            db,
        )

    @staticmethod
    def verify_payment(
        tx_ref: str,
        transaction_id: str,
        db: Session,
    ):
        return PaymentService.verify_order_payment(
            transaction_id,
            tx_ref,
            db,
        )
