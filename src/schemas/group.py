import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class GroupAddRequestDTO(BaseModel):
    title: Optional[str] = Field(None, max_length=599)
    category: Optional[str] = Field(None, max_length=599)
    user_quantity: Optional[int] = Field(None, max_length=3)
    date_from: Optional[datetime] = Field(None)
    date_end: Optional[datetime] = Field(None)
    period: Optional[str] = Field(None)


class GroupResponseDTO(BaseModel):
    id: uuid.UUID
    title: Optional[str] = Field(None, max_length=599)
    category: Optional[str] = Field(None, max_length=599)
    user_quantity: Optional[int] = Field(None, max_length=3)
    date_from: Optional[datetime] = Field(None)
    date_end: Optional[datetime] = Field(None)
    period: Optional[str] = Field(None)
    is_active: bool | None = True


class GroupAddDTO(BaseModel):
    id: uuid.UUID
    title: Optional[str] = Field(None, max_length=599)
    category: Optional[str] = Field(None, max_length=599)
    user_quantity: Optional[int] = Field(None, max_length=3)
    date_from: Optional[datetime] = Field(None)
    date_end: Optional[datetime] = Field(None)
    period: Optional[str] = Field(None)
    is_active: bool | None = True


class GroupPatchDTO(BaseModel):
    title: Optional[str] = Field(None, max_length=599)
    category: Optional[str] = Field(None, max_length=599)
    user_quantity: Optional[int] = Field(None, max_length=3)
    date_from: Optional[datetime] = Field(None)
    date_end: Optional[datetime] = Field(None)
    period: Optional[str] = Field(None)
    is_active: bool | None = None


class GroupDTO(BaseModel):
    id: uuid.UUID
    title: Optional[str] = Field(None, max_length=599)
    category: Optional[str] = Field(None, max_length=599)
    user_quantity: Optional[int] = Field(None, max_length=3)
    date_from: Optional[datetime] = Field(None)
    date_end: Optional[datetime] = Field(None)
    period: Optional[str] = Field(None)
    is_active: bool | None = None

    model_config = ConfigDict(from_attributes=True)
