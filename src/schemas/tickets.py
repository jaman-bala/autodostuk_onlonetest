import uuid
from pydantic import BaseModel, ConfigDict


class TicketAddRequest(BaseModel):
    title: str | None = None


class TicketResponse(BaseModel):
    id: uuid.UUID
    title: str | None = None


class TicketAdd(BaseModel):
    id: uuid.UUID
    title: str | None = None


class TicketPatch(BaseModel):
    title: str | None = None


class Ticket(BaseModel):
    id: uuid.UUID
    title: str | None = None

    model_config = ConfigDict(from_attributes=True)
