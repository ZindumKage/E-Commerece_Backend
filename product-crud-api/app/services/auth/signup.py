from datetime import (
    datetime,
    timedelta,
    timezone,
)

import logging
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.auth.token_hash import hash_token

from app.models.user import User

from app.utils.username_suggestions import (
    generate_username_suggestions,
)

from app.utils.mail import (
    send_verification_email,
)

from config.verification_token_generator import (
    generate_verification_token,
)

logger = logging.getLogger(__name__)


async def signup_service(
    db: Session,
    user,
):

    # CHECK EMAIL
    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    # CHECK USERNAME
    existing_username = db.query(User).filter(User.username == user.username).first()

    if existing_username:

        suggestions = generate_username_suggestions(
            db,
            user.username,
        )

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Username already exists",
                "suggestions": suggestions,
            },
        )

    # GENERATE VERIFICATION CODE
    raw_verification_token = generate_verification_token()

    # CREATE USER
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        # NEVER TRUST CLIENT ROLE
        role="user",
        is_verified=False,
        verification_token=hash_token(raw_verification_token),
        verification_token_expires_at=(
            datetime.now(timezone.utc) + timedelta(minutes=10)
        ),
    )

    try:

       db.add(new_user)

       db.commit()

       db.refresh(new_user)

    except IntegrityError:

       db.rollback()

       raise HTTPException(
        status_code=400,
        detail="Username or email already exists",
    )

    except Exception as e:

      db.rollback()

      logger.error(
        f"Database error during signup: {e}"
    )

      raise HTTPException(
        status_code=500,
        detail="Failed to create user",
    )

    # SEND VERIFICATION EMAIL
    try:

        await send_verification_email(
            new_user.email,
            raw_verification_token,
        )

    except Exception as e:

        logger.error(f"Failed to send verification email: {e}")

    return new_user
