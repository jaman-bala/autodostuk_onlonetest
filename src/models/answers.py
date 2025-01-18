import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, ForeignKey, String

from src.database import Base


# TODO: Модель ответа
class AnswerOrm(Base):
    __tablename__ = "answers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title_ru: Mapped[str | None] = mapped_column(String(999))  # TODO: Текст ответа на русском
    title_kg: Mapped[str | None] = mapped_column(String(999))  # TODO: Текст ответа на кыргызском
    is_correct: Mapped[bool | None] = mapped_column(Boolean, default=False)
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("questions.id", ondelete="CASCADE")
    )  # TODO: Связь с вопросом
