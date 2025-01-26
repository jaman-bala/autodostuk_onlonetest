import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


class AnswerAddRequestDTO(BaseModel):
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    is_correct: bool = False
    question_id: uuid.UUID

    @field_validator("title_ru", "title_kg")
    def check_empty_fields(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        if value is not None and value.strip() == "":
            raise ValueError("Field cannot be an empty string")
        return value


class AnswerResponseDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    is_correct: bool = False
    question_id: uuid.UUID


class AnswerAddDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    is_correct: bool = False
    question_id: uuid.UUID


class AnswerPatchDTO(BaseModel):
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    is_correct: Optional[bool] = False
    question_id: Optional[uuid.UUID]


class AnswerDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(None, max_length=999)
    title_kg: Optional[str] = Field(None, max_length=999)
    is_correct: bool = False
    question_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
