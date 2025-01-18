import uuid
from pydantic import BaseModel, ConfigDict


class ThemeAddRequest(BaseModel):
    title_ru: str | None = None
    title_kg: str | None = None


class ThemeResponse(BaseModel):
    id: uuid.UUID
    title_ru: str | None = None
    title_kg: str | None = None


class ThemeAdd(BaseModel):
    id: uuid.UUID
    title_ru: str | None = None
    title_kg: str | None = None


class ThemePatch(BaseModel):
    title_ru: str | None = None
    title_kg: str | None = None


class Theme(BaseModel):
    id: uuid.UUID
    title_ru: str | None = None
    title_kg: str | None = None

    model_config = ConfigDict(from_attributes=True)
