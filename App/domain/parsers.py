"""Parse standard WhatsApp messages into CalendarEvent.
Accepted formats (examples):
1) ADD: 2025-09-10 14:00-15:00 | Sessão terapia | Rua X, 123
2) EDIT: <EVENT_ID> | 2025-09-10 15:00-16:00 | Novo título | Nova descrição
3) HELP
"""

from datetime import datetime
from typing import Optional
from .models import CalendarEvent


SEP = "|"


class ParseError(ValueError):
    pass


class MessageParser:
    @staticmethod
    def _parse_datetime_range(s: str) -> tuple[datetime, datetime]:
        # "2025-09-10 14:00-15:00"
        date_part, times = s.strip().split(" ", 1)
        start_s, end_s = times.split("-")
        start = datetime.fromisoformat(f"{date_part}T{start_s}")
        end = datetime.fromisoformat(f"{date_part}T{end_s}")
        if end <= start:
            raise ParseError("end must be after start")
        return start, end


    @classmethod
    def parse_add(cls, body: str) -> CalendarEvent:
        # ADD: <date time-range> | <summary> | <description?>
        try:
            _, rest = body.split(":", 1)
            parts = [p.strip() for p in rest.split(SEP)]
            if len(parts) < 2:
                raise ParseError("Use: ADD: YYYY-MM-DD HH:MM-HH:MM | Título | Descrição(opcional)")
            start, end = cls._parse_datetime_range(parts[0])
            summary = parts[1]
            description: Optional[str] = parts[2] if len(parts) > 2 else None
            return CalendarEvent(summary=summary, start=start, end=end, description=description)
        except Exception as e:
            raise ParseError(str(e))


    @classmethod
    def parse_edit(cls, body: str) -> CalendarEvent:
        # EDIT: <event_id> | <date time-range?> | <summary?> | <description?>
        try:
            _, rest = body.split(":", 1)
            parts = [p.strip() for p in rest.split(SEP)]
            if len(parts) < 2:
                raise ParseError("Use: EDIT: EVENT_ID | YYYY-MM-DD HH:MM-HH:MM | Novo título | Nova descrição")
            event_id = parts[0]
            start, end, summary, description = None, None, None, None
            if len(parts) >= 2 and parts[1]:
                start, end = cls._parse_datetime_range(parts[1])
            if len(parts) >= 3 and parts[2]:
                summary = parts[2]
            if len(parts) >= 4 and parts[3]:
                description = parts[3]
            return CalendarEvent(summary=summary or "", start=start, end=end, description=description, event_id=event_id)
        except Exception as e:
            raise ParseError(str(e))