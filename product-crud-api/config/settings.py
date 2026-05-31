from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str

    DEBUG: bool

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_FROM: str
    BASE_URL: str
    FLUTTERWAVE_SECRET_KEY: str
    FLUTTERWAVE_PUBLIC_KEY: str
    FLUTTERWAVE_ENCRYPTION_KEY: str
    FLUTTERWAVE_BASE_URL: str
    FLUTTERWAVE_WEBHOOK_SECRET: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")


settings = Settings()
