from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.token_hash import hash_token

from app.helper.time_helper import ensure_utc

from app.models.user import User


def verify_email_service(
    db: Session,
    token: str,
):
    hashed_token = hash_token(token)

    user = (
        db.query(User)
        .filter(User.verification_token == hashed_token)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
        )

    expiry = ensure_utc(
        user.verification_token_expires_at
    )

    if expiry < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Verification token expired",
        )

    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires_at = None

    db.commit()

    return {
        "message": "Email verified successfully"
    }