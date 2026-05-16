from datetime import datetime, timedelta, timezone
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app.auth.token_hash import hash_token
from app.database import get_db
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user import (
    TokenResponse,
    UserResponse,
    UserSignUp,
)
from app.utils.mail import (
    send_reset_mail,
    send_verification_email,
)
from app.helper.time_helper import ensure_utc
from config.redis import redis_client
from config.settings import settings
from config.verification_token_generator import generate_verification_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =========================
# Schemas
# =========================


class RefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    new_password: str


# =========================
# Signup
# =========================


@router.post("/signup", response_model=UserResponse)
async def signup(user: UserSignUp, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    raw_verification_token = generate_verification_token()

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role="user",
        is_verified=False,
        # store hashed token
        verification_token=hash_token(raw_verification_token),
        # token expiry
        verification_token_expires_at=(
            datetime.now(timezone.utc) + timedelta(hours=24)
        ),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        await send_verification_email(new_user.email, raw_verification_token)

    except Exception as e:
        logger.error(f"Failed to send verification email: {e}")

    return new_user


# =========================
# Login
# =========================


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == form_data.username).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not existing_user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email first")

    access_token = create_access_token(
        {
            "id": existing_user.id,
            "role": existing_user.role,
        }
    )

    refresh_token = create_refresh_token(existing_user.id)

    db_refresh = RefreshToken(
        token=hash_token(refresh_token),
        user_id=existing_user.id,
        expires_at=(datetime.now(timezone.utc) + timedelta(days=3)),
        is_revoked=False,
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# =========================
# Refresh Token
# =========================


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
):
    refresh_token = payload.refresh_token

    try:
        decoded_payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if decoded_payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = decoded_payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        stored_token = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token == hash_token(refresh_token),
                RefreshToken.is_revoked == False,
            )
            .first()
        )

        if not stored_token:
            raise HTTPException(status_code=401, detail="Refresh token revoked")

        refresh_expiry = ensure_utc(stored_token.expires_at)

        if refresh_expiry < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # revoke old refresh token
        stored_token.is_revoked = True

        user = db.query(User).filter(User.id == int(user_id)).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # create new access token
        new_access_token = create_access_token(
            {
                "id": user.id,
                "role": user.role,
            }
        )

        # rotate refresh token
        new_refresh_token = create_refresh_token(user.id)

        db_refresh = RefreshToken(
            token=hash_token(new_refresh_token),
            user_id=user.id,
            expires_at=(datetime.now(timezone.utc) + timedelta(days=3)),
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
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# =========================
# Logout
# =========================


@router.post("/logout")
def logout(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
):
    refresh_token = payload.refresh_token

    # revoke in DB
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == hash_token(refresh_token))
        .first()
    )

    if db_token:
        db_token.is_revoked = True
        db.commit()

    # optional redis blacklist
    redis_client.set(refresh_token, "blacklisted", ex=60 * 60 * 24 * 3)

    return {"message": "Logged out successfully"}


# =========================
# Verify Email
# =========================


@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    hashed_token = hash_token(token)

    user = db.query(User).filter(User.verification_token == hashed_token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    expiry = ensure_utc(user.verification_token_expires_at)

    if expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Verification token expired")

    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires_at = None

    db.commit()

    return {"message": "Email verified successfully"}


# =========================
# Forgot Password
# =========================


@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == payload.email).first()

    # prevent email enumeration
    if user:
        raw_reset_token = generate_verification_token()

        user.reset_token = hash_token(raw_reset_token)

        user.reset_token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        db.commit()

        try:
            await send_reset_mail(user.email, raw_reset_token)

        except Exception as e:
            logger.error(f"Failed to send reset email: {e}")

    return {"message": "If the email exists, a reset link has been sent"}


# =========================
# Reset Password
# =========================


@router.post("/reset-password/{token}")
def reset_password(
    token: str,
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    hashed_token = hash_token(token)

    user = db.query(User).filter(User.reset_token == hashed_token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    reset_expiry = ensure_utc(user.reset_token_expires_at)

    if reset_expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset token expired")

    user.password = hash_password(payload.new_password)

    user.reset_token = None
    user.reset_token_expires_at = None

    db.commit()

    return {"message": "Password reset successful"}
