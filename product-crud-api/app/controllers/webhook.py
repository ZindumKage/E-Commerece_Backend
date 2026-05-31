from fastapi import Request
from sqlalchemy.orm import Session

from app.services.webhook import WebhookService


class WebhookController:
    @staticmethod
    async def flutterwave_webhook(
        request: Request,
        db: Session,
    ):
        return await WebhookService.handle_flutterwave_webhook(
            request,
            db
        )