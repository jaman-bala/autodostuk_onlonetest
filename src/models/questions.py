import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import String, ForeignKey

from src.database import Base


# TODO: Модель вопроса
class QuestionOrm(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title_ru: Mapped[str | None] = mapped_column(
        String(999)
    )  # TODO: Заголовок или краткое описание вопросов на русском
    title_kg: Mapped[str | None] = mapped_column(
        String(999)
    )  # TODO: Заголовок или краткое описание вопросов на кыргызском
    description_ru: Mapped[str | None] = mapped_column(
        String()
    )  # TODO: Полное описание вопросов на русском
    description_kg: Mapped[str | None] = mapped_column(
        String()
    )  # TODO: Полное описание вопросов нв киргызском
    files: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )  # TODO Вставка файлов
    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE")
    )  # TODO: Связь с билетом
    theme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("themes.id", ondelete="CASCADE")
    )  # TODO: Связь с темой
