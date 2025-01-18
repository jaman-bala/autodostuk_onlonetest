import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, ForeignKey, Integer
from datetime import datetime

from src.database import Base


class ReportOrm(Base):
    __tablename__ = "reports"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"), nullable=True, default=None
    )
    theme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("themes.id", ondelete="CASCADE"), nullable=True, default=None
    )
    points: Mapped[int | None] = mapped_column(Integer)
    date_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    date_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
