# app/utils/mail.py

from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
)

from config.settings import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_verification_email(
    email: str,
    token: str,
):

    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"""

Your email verification code is:

{token}

This code expires in 10 minutes.



        """,
        subtype="plain",
    )

    fm = FastMail(conf)

    await fm.send_message(message)


async def send_reset_mail(
    email: str,
    token: str,
):

    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email],
        body=f"""

Your password reset code is:

{token}

This code expires in 10 minutes.



        """,
        subtype="plain",
    )

    fm = FastMail(conf)

    await fm.send_message(message)