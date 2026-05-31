from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
)

from app.auth.token_hash import hash_token

from app.helper.time_helper import ensure_utc

from app.models.refresh_token import RefreshToken
from app.models.user import User

from config.redis import redis_client
from config.settings import settings


def refresh_token_service(
    db: Session,
    refresh_token: str,
):
    try:
        decoded_payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if decoded_payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type",
            )

        user_id = decoded_payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
            )

        stored_token = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token == hash_token(refresh_token),
                RefreshToken.is_revoked == False,
            )
            .first()
        )

        if not stored_token:
            raise HTTPException(
                status_code=401,
                detail="Refresh token revoked",
            )

        refresh_expiry = ensure_utc(
            stored_token.expires_at
        )

        if refresh_expiry < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=401,
                detail="Refresh token expired",
            )

        # revoke old token
        stored_token.is_revoked = True

        user = (
            db.query(User)
            .filter(User.id == int(user_id))
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        # create new access token
        new_access_token = create_access_token(
            {
                "id": user.id,
                "role": user.role,
            }
        )

        # rotate refresh token
        new_refresh_token = create_refresh_token(
            user.id
        )

        db_refresh = RefreshToken(
            token=hash_token(new_refresh_token),
            user_id=user.id,
            expires_at=(
                datetime.now(timezone.utc)
                + timedelta(days=3)
            ),
            is_revoked=False,
        )

        db.add(db_refresh)
        db.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )


def logout_service(
    db: Session,
    refresh_token: str,
):
    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == hash_token(refresh_token)
        )
        .first()
    )

    if db_token:
        db_token.is_revoked = True
        db.commit()

    redis_client.set(
        refresh_token,
        "blacklisted",
        ex=60 * 60 * 24 * 3,
    )

    return {
        "message": "Logged out successfully"
    }