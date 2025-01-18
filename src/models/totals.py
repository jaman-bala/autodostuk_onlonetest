import uuid
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, Date
from datetime import date

from src.database import Base


# TODO: Модель финальный экзамен
class TotalOrm(Base):
    __tablename__ = "totals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    points: Mapped[int | None] = mapped_column(Integer)
    date_from: Mapped[date | None] = mapped_column(Date)
    date_end: Mapped[date | None] = mapped_column(Date)

    @hybrid_property
    def duration_in_days(self):
        """Вычисляет длительность обучения в днях."""
        if self.date_from and self.date_end:
            return (self.date_end - self.date_from).days
        return None

    @hybrid_property
    def is_valid_date_range(self):
        """Проверяет, что дата окончания позже или равна дате начала."""
        if self.date_from and self.date_end:
            return self.date_end >= self.date_from
        return False
