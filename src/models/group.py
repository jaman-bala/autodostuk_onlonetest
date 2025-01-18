import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Integer, String, Date
from datetime import date


from src.database import Base


# TODO: Модель Группы
class GroupOrm(Base):
    __tablename__ = "groups"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str | None] = mapped_column(String(599), unique=True)
    category: Mapped[str | None] = mapped_column(String(599))
    user_quantity: Mapped[int | None] = mapped_column(Integer, default=0)
    date_from: Mapped[date] = mapped_column(Date)
    date_end: Mapped[date] = mapped_column(Date)
    period: Mapped[str | None] = mapped_column(String())  # TODO период обучения
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # TODO: Активность группы

    users = relationship("UsersOrm", back_populates="group", cascade="all, delete-orphan")
