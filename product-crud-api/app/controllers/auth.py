from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import (
    RefreshRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from app.schemas.user import (
    UserSignUp,
    UserResponse,
    TokenResponse,
)

from app.services.auth.login import login_service
from app.services.auth.signup import signup_service

from app.services.auth.username import check_username_service

from app.services.auth.password import (
    forgot_password_service,
    reset_password_service,
)

from app.services.auth.token import (
    refresh_token_service,
    logout_service,
)

from app.services.auth.verification import (
    verify_email_service,
)


async def signup(
    user: UserSignUp,
    db: Session = Depends(get_db),
) -> UserResponse:

    return await signup_service(
        db,
        user,
    )


def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:

    return login_service(
        db,
        form_data,
    )


def refresh_access_token(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:

    return refresh_token_service(
        db,
        payload.refresh_token,
    )


def logout(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
) -> dict:

    return logout_service(
        db,
        payload.refresh_token,
    )


def verify_email(
    token: str,
    db: Session = Depends(get_db),
) -> dict:

    return verify_email_service(
        db,
        token,
    )


async def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
) -> dict:

    return await forgot_password_service(
        db,
        payload.email,
    )


def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
) -> dict:

    return reset_password_service(
        db,
        payload.token,
        payload.new_password,
    )


def check_username(username: str, db: Session = Depends(get_db)):
    return check_username_service(db, username)
