from datetime import datetime
import zoneinfo
from ..config import get_settings
from .calendar_service import GoogleCalendarService
from .whatsapp_service import WhatsAppService


class AgendaService:
    def __init__(self):
        self.settings = get_settings()
        self.cal = GoogleCalendarService()
        self.wa = WhatsAppService()


    def send_today(self) -> None:
        now = datetime.now(tz=zoneinfo.ZoneInfo(self.settings.TZ))
        agenda = self.cal.get_today_agenda(now)
        text = self.cal.render_agenda_text(agenda)
        self.wa.send_text(self.settings.RECIPIENT_PHONE_E164, text)