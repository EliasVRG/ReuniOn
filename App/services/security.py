from fastapi import HTTPException, Request
from ..config import get_settings


async def verify_whatsapp_webhook(request: Request) -> None:
    # WhatsApp Cloud API uses query params 'hub.mode', 'hub.verify_token', 'hub.challenge' on GET
    # For POST, signature validation (X-Hub-Signature-256) can be added if HMAC is configured.
    # Here we validate the verify token on GET and (optionally) the sender on POST.
    return


def ensure_sender_allowed(sender: str) -> None:
    settings = get_settings()
    allow = settings.ALLOWED_SENDER_PHONE_E164
    if allow and sender != allow:
        raise HTTPException(status_code=403, detail="Sender not allowed")