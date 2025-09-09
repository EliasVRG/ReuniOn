from __future__ import annotations
from datetime import datetime, timedelta
from typing import Iterable
import google.oauth2.credentials as oauth2
from googleapiclient.discovery import build
from ..config import get_settings
from ..domain.models import CalendarEvent, Agenda, AgendaItem


SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarService:
    def __init__(self):
        self.settings = get_settings()
        self.creds = oauth2.Credentials(
            None,
            refresh_token=self.settings.GOOGLE_REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.settings.GOOGLE_CLIENT_ID,
            client_secret=self.settings.GOOGLE_CLIENT_SECRET,
            scopes=SCOPES,
        )
        self.service = build("calendar", "v3", credentials=self.creds, cache_discovery=False)


    @property
    def calendar_id(self) -> str:
        return self.settings.GOOGLE_CALENDAR_ID


    def add_event(self, ev: CalendarEvent) -> str:
        body = {
            "summary": ev.summary,
            "description": ev.description,
            "start": {"dateTime": ev.start.isoformat(), "timeZone": ev.timezone},
            "end": {"dateTime": ev.end.isoformat(), "timeZone": ev.timezone},
        }
        res = self.service.events().insert(calendarId=self.calendar_id, body=body).execute()
        return res["id"]


    def edit_event(self, ev: CalendarEvent) -> str:
        assert ev.event_id, "event_id required"
        orig = self.service.events().get(calendarId=self.calendar_id, eventId=ev.event_id).execute()
        # patch fields if provided
        if ev.summary:
            orig["summary"] = ev.summary
        if ev.description is not None:
            orig["description"] = ev.description
        if ev.start:
            orig["start"] = {"dateTime": ev.start.isoformat(), "timeZone": ev.timezone}
        if ev.end:
            orig["end"] = {"dateTime": ev.end.isoformat(), "timeZone": ev.timezone}
            res = self.service.events().update(calendarId=self.calendar_id, eventId=ev.event_id, body=orig).execute()
        return res["id"]

    def get_today_agenda(self, now: datetime) -> Agenda:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        events = (
            self.service.events()
            .list(
                calendarId=self.calendar_id,
                timeMin=start.isoformat() + "Z",
                timeMax=end.isoformat() + "Z",
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
            .get("items", [])
        )
        items: list[AgendaItem] = []
        for e in events:
            st = e.get("start", {}).get("dateTime") or e.get("start", {}).get("date")
            en = e.get("end", {}).get("dateTime") or e.get("end", {}).get("date")
            if st and en:
                items.append(AgendaItem(start=datetime.fromisoformat(st.replace("Z","+00:00")),
                                        end=datetime.fromisoformat(en.replace("Z","+00:00")),
                                        summary=e.get("summary", "(sem título)")))
        return Agenda(date=start, items=items)


    @staticmethod
    def render_agenda_text(agenda: Agenda) -> str:
        if not agenda.items:
            return "Agenda de hoje: sem eventos."
        lines = ["Agenda de hoje:"]
        for it in agenda.items:
            lines.append(f"- {it.start.strftime('%H:%M')}–{it.end.strftime('%H:%M')} {it.summary}")
        return "\n".join(lines)