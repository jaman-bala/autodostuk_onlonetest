import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo
from datetime import datetime


class ReportAddRequestDTO(BaseModel):
    user_id: uuid.UUID
    ticket_id: Optional[uuid.UUID] = Field(None)
    theme_id: Optional[uuid.UUID] = Field(None)
    points: Optional[int] = Field(None)
    date_from: datetime
    date_end: datetime

    @field_validator("date_end")
    def check_dates(cls, value: datetime, info: ValidationInfo) -> datetime:
        if value <= info.data["date_from"]:
            raise ValueError("date_end must be after date_from")
        return value

    @field_validator("points")
    def check_points(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value < 0:
            raise ValueError("points must be a positive integer")
        return value


class ReportResponseDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ticket_id: Optional[uuid.UUID] = Field(None)
    theme_id: Optional[uuid.UUID] = Field(None)
    points: Optional[int] = Field(None)
    date_from: datetime
    date_end: datetime


class ReportAddDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ticket_id: Optional[uuid.UUID] = Field(None)
    theme_id: Optional[uuid.UUID] = Field(None)
    points: Optional[int] = Field(None)
    date_from: datetime
    date_end: datetime


class ReportPatchDTO(BaseModel):
    user_id: uuid.UUID
    ticket_id: Optional[uuid.UUID] = Field(None)
    theme_id: Optional[uuid.UUID] = Field(None)
    points: Optional[int] = Field(None)
    date_from: datetime
    date_end: datetime


class ReportDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ticket_id: Optional[uuid.UUID] = Field(None)
    theme_id: Optional[uuid.UUID] = Field(None)
    points: Optional[int] = Field(None)
    date_from: datetime
    date_end: datetime

    model_config = ConfigDict(from_attributes=True)
