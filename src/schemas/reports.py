import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ReportAddRequest(BaseModel):
    user_id: uuid.UUID
    ticket_id: uuid.UUID | None = None
    theme_id: uuid.UUID | None = None
    points: int | None = None
    date_from: datetime
    date_end: datetime


class ReportResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ticket_id: uuid.UUID | None = None
    theme_id: uuid.UUID | None = None
    points: int | None = None
    date_from: datetime
    date_end: datetime


class ReportAdd(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ticket_id: uuid.UUID | None = None
    theme_id: uuid.UUID | None = None
    points: int | None = None
    date_from: datetime
    date_end: datetime


class ReportPatch(BaseModel):
    user_id: uuid.UUID
    ticket_id: uuid.UUID | None = None
    theme_id: uuid.UUID | None = None
    points: int | None = None
    date_from: datetime
    date_end: datetime


class Report(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ticket_id: uuid.UUID | None = None
    theme_id: uuid.UUID | None = None
    points: int | None = None
    date_from: datetime
    date_end: datetime

    model_config = ConfigDict(from_attributes=True)
