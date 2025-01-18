import uuid
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class TotalAddRequest(BaseModel):
    user_id: uuid.UUID
    points: int | None = None
    date_from: date | None = None
    date_end: date | None = None


class TotalResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    points: int | None = None
    date_from: date | None = None
    date_end: date | None = None


class TotalAdd(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    points: int | None = None
    date_from: date | None = None
    date_end: date | None = None
    created_date: datetime
    updated_date: datetime


class TotalPatch(BaseModel):
    user_id: uuid.UUID
    points: int | None = None
    date_from: date | None = None
    date_end: date | None = None


class Total(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    points: int | None = None
    date_from: date | None = None
    date_end: date | None = None

    model_config = ConfigDict(from_attributes=True)
