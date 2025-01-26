import uuid
from typing import Optional
from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


class TotalAddRequestDTO(BaseModel):
    user_id: uuid.UUID
    points: Optional[int] = Field(None)
    date_from: date
    date_end: date

    @field_validator("points")
    def check_points(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("Points must be a positive integer")
        return value

    @field_validator("date_end")
    def check_dates(cls, value: date, info: ValidationInfo) -> date:
        if value is not None and info.data.get("date_from") is not None:
            if value < info.data["date_from"]:
                raise ValueError("date_end must be after or equal to date_from")
        return value


class TotalResponseDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    points: Optional[int] = Field(None)
    date_from: date
    date_end: date


class TotalAddDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    points: int | None = None
    date_from: date | None = None
    date_end: date | None = None


class TotalPatchDTO(BaseModel):
    user_id: uuid.UUID
    points: Optional[int] = Field(None)
    date_from: date
    date_end: date


class TotalDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    points: Optional[int] = Field(None)
    date_from: date
    date_end: date

    model_config = ConfigDict(from_attributes=True)
