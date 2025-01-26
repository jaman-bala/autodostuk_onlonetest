import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo
from datetime import date


class PaymentAddRequestDTO(BaseModel):
    user_id: uuid.UUID
    date_check: date
    price: Optional[int] = Field(None)

    @field_validator("price")
    def check_price(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("Price must be a positive integer")
        return value

    @field_validator("date_check")
    def check_date(cls, value: date, info: ValidationInfo) -> date:
        if value > date.today():
            raise ValueError("The date cannot be in the future")
        return value


class PaymentResponseDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    date_check: date
    price: Optional[int] = Field(None)


class PaymentAddDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    date_check: date
    price: Optional[int] = Field(None)


class PaymentPatchDTO(BaseModel):
    user_id: uuid.UUID
    date_check: date
    price: Optional[int] = Field(None)


class PaymentDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    date_check: date
    price: Optional[int] = Field(None)

    model_config = ConfigDict(from_attributes=True)
