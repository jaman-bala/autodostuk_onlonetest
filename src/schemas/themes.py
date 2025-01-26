import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


class ThemeAddRequestDTO(BaseModel):
    title_ru: Optional[str] = Field(max_length=599)
    title_kg: Optional[str] = Field(max_length=599)


class ThemeResponseDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(max_length=599)
    title_kg: Optional[str] = Field(max_length=599)

    @field_validator("title_ru", "title_kg")
    def check_empty_fields(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        if value is not None and value.strip() == "":
            raise ValueError(f"{info.field_name} cannot be an empty string")
        return value


class ThemeAddDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(max_length=599)
    title_kg: Optional[str] = Field(max_length=599)


class ThemePatchDTO(BaseModel):
    title_ru: Optional[str] = Field(max_length=599)
    title_kg: Optional[str] = Field(max_length=599)


class ThemeDTO(BaseModel):
    id: uuid.UUID
    title_ru: Optional[str] = Field(max_length=599)
    title_kg: Optional[str] = Field(max_length=599)

    model_config = ConfigDict(from_attributes=True)
