from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from .config import get_settings
from .services.whatsapp_service import WhatsAppService
from .services.calendar_service import GoogleCalendarService
from .domain.parsers import MessageParser, ParseError
from .services.security import ensure_sender_allowed
from .tasks.daily_agenda import run_daily_agenda
from .utils.logging import logger


app = FastAPI(title="WhatsApp Calendar Automation")


@app.get("/health")
def health():
    return {"ok": True}

@app.get("/whatsapp/webhook")
def whatsapp_verify(mode: str | None = None, hub_challenge: str | None = None, hub_verify_token: str | None = None, **kwargs):
    # Meta expects hub.mode, hub.verify_token, hub.challenge
    settings = get_settings()
    if hub_verify_token != settings.WABA_VERIFY_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid verify token")
    return PlainTextResponse(hub_challenge or "OK")


@app.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    settings = get_settings()
    body = await request.json()
    # Minimal extraction (for a single recipient model)
    try:
        entry = body["entry"][0]["changes"][0]["value"]["messages"][0]
        from_phone = entry["from"] # E.164 without '+'
        text = entry.get("text", {}).get("body", "").strip()
    except Exception:
        return {"ignored": True}


    # Optionally restrict allowed sender
    ensure_sender_allowed("+" + from_phone)


    wa = WhatsAppService()


    if text.upper().startswith("HELP"):
        wa.send_text(settings.RECIPIENT_PHONE_E164, wa.format_help())
        return {"ok": True}


    if text.upper().startswith("AGENDA"):
        run_daily_agenda()
        return {"ok": True}


    cal = GoogleCalendarService()


    try:
        if text.upper().startswith("ADD:"):
            ev = MessageParser.parse_add(text)
            ev_id = cal.add_event(ev)
            wa.send_text(settings.RECIPIENT_PHONE_E164, f"Evento criado. ID: {ev_id}")
            return {"ok": True, "event_id": ev_id}
        elif text.upper().startswith("EDIT:"):
            ev = MessageParser.parse_edit(text)
            if not ev.event_id:
                raise ParseError("event_id obrigatório")
            ev_id = cal.edit_event(ev)
            wa.send_text(settings.RECIPIENT_PHONE_E164, f"Evento atualizado. ID: {ev_id}")
            return {"ok": True, "event_id": ev_id}
        else:
            wa.send_text(settings.RECIPIENT_PHONE_E164, "Comando não reconhecido. Envie HELP.")
            return {"ok": False, "error": "unknown_command"}
    except ParseError as e:
        wa.send_text(settings.RECIPIENT_PHONE_E164, f"Erro de formato: {e}")
        return {"ok": False, "error": str(e)}

@app.get("/tasks/send_daily")
def task_send_daily():
    return run_daily_agenda()