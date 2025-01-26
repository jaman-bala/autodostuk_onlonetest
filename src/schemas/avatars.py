import uuid

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AvatarRequestAddDTO(BaseModel):
    filename: str | None = None
    file_path: str | None = None


class AvatarAddDTO(BaseModel):
    id: int
    file_path: str | None = None


class AvatarDTO(BaseModel):
    id: int
    file_path: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ImagesAddRequestDTO(BaseModel):
    path: str | None = None


class ImagesAddDTO(BaseModel):
    path: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ImagesPatchDTO(BaseModel):
    path: str | None = None


class ImagesDTO(BaseModel):
    id: uuid.UUID
    path: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class QuestionsImagesAddDTO(BaseModel):
    question_id: uuid.UUID
    image_id: uuid.UUID


class QuestionsImagesDTO(BaseModel):
    id: uuid.UUID
    question_id: uuid.UUID
    image_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
