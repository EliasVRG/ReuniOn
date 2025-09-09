from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class IncomingMessage(BaseModel):
    from_phone: str
    body: str
    timestamp: Optional[datetime] = None


class CalendarEvent(BaseModel):
    summary: str
    start: datetime
    end: datetime
    description: Optional[str] = None
    timezone: str = Field(default="America/Sao_Paulo")
    event_id: Optional[str] = None # when editing


class AgendaItem(BaseModel):
    start: datetime
    end: datetime
    summary: str


class Agenda(BaseModel):
    date: datetime
    items: list[AgendaItem]