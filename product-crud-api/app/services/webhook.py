from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.models.order import Order
from config.settings import settings

class WebhookService:
    @staticmethod
    async def handle_flutterwave_webhook(
        request: Request,
        db: Session
    ):
        secret_hash = request.headers.get("verif-hash")
        
        if secret_hash != settings.FLUTTERWAVE_WEBHOOK_SECRET:
            raise HTTPException(
                status_code=401,
                detail="Invalid webhook signature",
            )
            
        payload = await request.json()
        event = payload.get("event")
        
        if event != "charge.completed":
            return {"message": "Event Ignored"}
        
        data = payload.get("data", {})
        
        tx_ref = data.get("tx_ref")
        status = data.get("status")
        amount = data.get("amount")
        
        order = (
            db.query(Order)
            .filter(Order.transaction_ref == tx_ref)
            .first()
        )
        
        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )
            
    # Prevent Duplicate Updates
        if order.status == "paid":
            return{
                "message": "Order already updated"
            }
        if float(amount) != float(order.total_price):
            raise HTTPException(
                status_code=400,
                detail="Amount mismatch"
            )
        if status == "successful":
            order.status = "paid"
        
        else:
            order.status = "failed"
            
        db.commit()
        db.refresh(order)
        
        return {
            "message": "Webhook processed Successfully"
        }
        
        