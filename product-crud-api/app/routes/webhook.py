from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.controllers.webhook import WebhookController
from app.database import get_db


router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
)


@router.post("/flutterwave")
async def flutterwave_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    return await WebhookController.flutterwave_webhook(
        request,
        db,
    )