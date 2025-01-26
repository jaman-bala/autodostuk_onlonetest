import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import String, ForeignKey

from src.database import Base


# TODO: Модель вопроса
class QuestionOrm(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title_ru: Mapped[str | None] = mapped_column(String(999))
    title_kg: Mapped[str | None] = mapped_column(String(999))
    description_ru: Mapped[str | None] = mapped_column(String())
    description_kg: Mapped[str | None] = mapped_column(String())
    files: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE")
    )
    theme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("themes.id", ondelete="CASCADE")
    )
