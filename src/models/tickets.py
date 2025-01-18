import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


# TODO: Модель билета
class TicketOrm(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str | None] = mapped_column(String(999))  # TODO: Название билета
