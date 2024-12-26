import uuid
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import ARRAY

from src.database import Base


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    lastname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    is_ready: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    roles: Mapped[List[Role]] = mapped_column(ARRAY(String))
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )  # TODO: Дата создание
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )  # TODO: Дата обновление

    group = relationship("GroupOrm", back_populates="users")
