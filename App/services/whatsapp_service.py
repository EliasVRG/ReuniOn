import httpx
from ..config import get_settings
from ..utils.logging import logger


class WhatsAppService:
    BASE_URL = "https://graph.facebook.com/v20.0"


    def __init__(self):
        self.settings = get_settings()
        self.session = httpx.Client(timeout=10)

    def send_text(self, to_e164: str, body: str) -> None:
        url = f"{self.BASE_URL}/{self.settings.WABA_PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {self.settings.WABA_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_e164,
            "type": "text",
            "text": {"body": body[:4000]}, # WA limit safety
        }
        r = self.session.post(url, headers=headers, json=payload)
        try:
            r.raise_for_status()
        except Exception as e:
            logger.error("WhatsApp send failed: %s - %s", e, r.text)
        raise


    def format_help(self) -> str:
        return (
            "Comandos:\n"
            "HELP — mostra este texto\n"
            "ADD: YYYY-MM-DD HH:MM-HH:MM | Título | Descrição(opcional)\n"
            "EDIT: EVENT_ID | YYYY-MM-DD HH:MM-HH:MM | Novo título | Nova descrição\n"
            "AGENDA — envia a agenda de hoje."
        )