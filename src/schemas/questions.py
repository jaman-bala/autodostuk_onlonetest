import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


class QuestionAddRequestDTO(BaseModel):
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    description_ru: Optional[str] = Field(None)
    description_kg: Optional[str] = Field(None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID

    @field_validator("title_ru", "title_kg", "description_ru", "description_kg")
    def check_empty_fields(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        if value is not None and value.strip() == "":
            raise ValueError("Field cannot be an empty string")
        return value


class QuestionResponseDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    description_ru: Optional[str] = Field(None)
    description_kg: Optional[str] = Field(None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID
    files: list[str] | None = None


class QuestionAddDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    description_ru: Optional[str] = Field(None)
    description_kg: Optional[str] = Field(None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID
    files: list[str] | None = None


class QuestionPatchDTO(BaseModel):
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    description_ru: Optional[str] = Field(None)
    description_kg: Optional[str] = Field(None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID


class QuestionPatchFileDTO(BaseModel):
    files: list[str] | None = None


class QuestionDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    description_ru: Optional[str] = Field(None)
    description_kg: Optional[str] = Field(None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID
    files: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)
