from datetime import datetime, timedelta, timezone
from operator import or_

from fastapi import HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy import or_

from app.auth.hashing import verify_password

from app.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
)

from app.auth.token_hash import hash_token

from app.models.refresh_token import RefreshToken
from app.models.user import User


def login_service(
    db: Session,
    form_data,
):
    existing_user = (
        db.query(User)
        .filter(
            or_(User.email == form_data.username,
                User.username == form_data.username,
            )
        )
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(
        form_data.password,
        existing_user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not existing_user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email first",
        )

    access_token = create_access_token(
        {
            "id": existing_user.id,
            "role": existing_user.role,
        }
    )

    refresh_token = create_refresh_token(
        existing_user.id
    )

    db_refresh = RefreshToken(
        token=hash_token(refresh_token),
        user_id=existing_user.id,
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(days=3)
        ),
        is_revoked=False,
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }