from pydantic import BaseSettings, Field
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "whatsapp-calendar-automation"
    ENV: str = "production"
    TZ: str = Field(default="America/Sao_Paulo")

    # WhatsApp Cloud API
    WABA_VERIFY_TOKEN: str # for webhook verification
    WABA_ACCESS_TOKEN: str # Bearer token for Graph API
    WABA_PHONE_NUMBER_ID: str
    RECIPIENT_PHONE_E164: str # e.g. +5511999999999 (the single user)


    # Google OAuth (Installed App or Web App) — using refresh token server-side
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REFRESH_TOKEN: str
    GOOGLE_CALENDAR_ID: str = "primary"


    # Daily agenda schedule
    DAILY_SEND_HOUR_LOCAL: int = 8 # 0-23 user local TZ
    DAILY_SEND_MINUTE_LOCAL: int = 0


    # Security
    ALLOWED_SENDER_PHONE_E164: str = "" # optional: restrict inbound


class Config:
    env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore[arg-type]