import uuid
from pydantic import BaseModel, ConfigDict


class AnswerAddRequest(BaseModel):
    title_ru: str | None = None
    title_kg: str | None = None
    is_correct: bool = False
    question_id: uuid.UUID


class AnswerResponse(BaseModel):
    id: uuid.UUID
    title_ru: str | None = None
    title_kg: str | None = None
    is_correct: bool = False
    question_id: uuid.UUID


class AnswerAdd(BaseModel):
    id: uuid.UUID
    title_ru: str | None = None
    title_kg: str | None = None
    is_correct: bool = False
    question_id: uuid.UUID


class AnswerPatch(BaseModel):
    title_ru: str | None = None
    title_kg: str | None = None
    is_correct: bool = False
    question_id: uuid.UUID


class Answer(BaseModel):
    id: uuid.UUID
    title_ru: str | None = None
    title_kg: str | None = None
    is_correct: bool = False
    question_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
