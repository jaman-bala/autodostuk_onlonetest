import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, Date

from src.database import Base


# TODO: Модель платежа
class PaymentOrm(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    date_check: Mapped[date] = mapped_column(Date)
    price: Mapped[int | None] = mapped_column(Integer, default=0)
