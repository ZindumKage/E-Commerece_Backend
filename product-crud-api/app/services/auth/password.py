from datetime import datetime, timedelta, timezone
import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.auth.token_hash import hash_token

from app.helper.time_helper import ensure_utc

from app.models.user import User

from app.utils.mail import send_reset_mail

from config.verification_token_generator import (
    generate_verification_token,
)

logger = logging.getLogger(__name__)


async def forgot_password_service(
    db: Session,
    email: str,
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # prevent email enumeration
    if user:
        raw_reset_token = (
            generate_verification_token()
        )

        user.reset_token = hash_token(
            raw_reset_token
        )

        user.reset_token_expires_at = (
            datetime.now(timezone.utc)
            + timedelta(minutes=10)
        )

        db.commit()

        try:
            await send_reset_mail(
                user.email,
                raw_reset_token,
            )

        except Exception as e:
            logger.error(
                f"Failed to send reset email: {e}"
            )

    return {
        "message": "If the email exists, a reset link has been sent"
    }


def reset_password_service(
    db: Session,
    token: str,
    new_password: str,
):
    hashed_token = hash_token(token)

    user = (
        db.query(User)
        .filter(User.reset_token == hashed_token)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
        )

    reset_expiry = ensure_utc(
        user.reset_token_expires_at
    )

    if reset_expiry < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Reset token expired",
        )

    user.password = hash_password(
        new_password
    )

    user.reset_token = None
    user.reset_token_expires_at = None

    db.commit()

    return {
        "message": "Password reset successful"
    }