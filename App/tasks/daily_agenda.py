from ..services.agenda_service import AgendaService


def run_daily_agenda() -> dict:
    svc = AgendaService()
    svc.send_today()
    return {"status": "ok"}