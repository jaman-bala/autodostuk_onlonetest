import uuid
from pydantic import BaseModel, ConfigDict, Field


class QuestionAddRequest(BaseModel):
    title_ru: str = Field(default=None, max_length=999)
    title_kg: str = Field(default=None, max_length=999)
    description_ru: str = Field(default=None)
    description_kg: str = Field(default=None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID


class QuestionResponse(BaseModel):
    id: uuid.UUID
    title_ru: str = Field(default=None, max_length=999)
    title_kg: str = Field(default=None, max_length=999)
    description_ru: str = Field(default=None)
    description_kg: str = Field(default=None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID
    files: list[str] | None = None


class QuestionAdd(BaseModel):
    id: uuid.UUID
    title_ru: str = Field(default=None, max_length=999)
    title_kg: str = Field(default=None, max_length=999)
    description_ru: str = Field(default=None)
    description_kg: str = Field(default=None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID
    files: list[str] | None = None


class QuestionPatch(BaseModel):
    title_ru: str = Field(default=None, max_length=999)
    title_kg: str = Field(default=None, max_length=999)
    description_ru: str = Field(default=None)
    description_kg: str = Field(default=None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID


class QuestionPatchFile(BaseModel):
    files: list[str] | None = None


class Question(BaseModel):
    id: uuid.UUID
    title_ru: str = Field(default=None, max_length=999)
    title_kg: str = Field(default=None, max_length=999)
    description_ru: str = Field(default=None)
    description_kg: str = Field(default=None)
    ticket_id: uuid.UUID
    theme_id: uuid.UUID
    files: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)
