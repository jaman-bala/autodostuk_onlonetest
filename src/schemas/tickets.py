import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


class TicketAddRequestDTO(BaseModel):
    title: Optional[str] = Field(None, max_length=999)

    @field_validator("title")
    def check_empty_field(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        if value is not None and value.strip() == "":
            raise ValueError(f"{info.field_name} cannot be an empty string")
        return value


class TicketResponseDTO(BaseModel):
    id: uuid.UUID
    title: Optional[str] = Field(None, max_length=999)


class TicketAddDTO(BaseModel):
    id: uuid.UUID
    title: Optional[str] = Field(None, max_length=999)


class TicketPatchDTO(BaseModel):
    title: Optional[str] = Field(None, max_length=999)


class TicketDTO(BaseModel):
    id: uuid.UUID
    title: Optional[str] = Field(None, max_length=999)

    model_config = ConfigDict(from_attributes=True)
