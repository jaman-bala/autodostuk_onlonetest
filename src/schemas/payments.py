import uuid
from pydantic import BaseModel, ConfigDict
from datetime import date


class PaymentAddRequest(BaseModel):
    user_id: uuid.UUID
    date_check: date
    price: int


class PaymentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    date_check: date
    price: int


class PaymentAdd(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    date_check: date
    price: int


class PaymentPatch(BaseModel):
    user_id: uuid.UUID
    date_check: date
    price: int


class Payment(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    date_check: date
    price: int

    model_config = ConfigDict(from_attributes=True)
