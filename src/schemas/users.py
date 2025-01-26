import uuid
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationInfo
from enum import Enum


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserRequestAddDTO(BaseModel):
    firstname: Optional[str] = Field(None, max_length=100)
    lastname: Optional[str] = Field(None, max_length=100)
    password: str = Field(min_length=1, max_length=200)
    phone: str = Field(min_length=1, max_length=20)
    is_ready: Optional[int] = Field(None)
    group_id: uuid.UUID = Field(None)
    is_active: bool = True
    roles: list[Role] = Field(default_factory=lambda: [Role.USER])

    @field_validator("firstname", "lastname")
    def check_empty_fields(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        if value is not None and value.strip() == "":
            raise ValueError(f"{info.field_name} cannot be an empty string")
        return value

    @field_validator("password", "phone")
    def check_length(cls, value: str, info: ValidationInfo) -> str:
        if not (1 <= len(value) <= 200):
            raise ValueError(
                f"Length of field {info.field_name} must be between 1 and 200 characters"
            )
        return value


class UserResponseDTO(BaseModel):
    id: uuid.UUID
    firstname: Optional[str] = Field(None, max_length=100)
    lastname: Optional[str] = Field(None, max_length=100)
    phone: str = Field(min_length=1, max_length=20)
    is_ready: Optional[int] = Field(None)
    group_id: uuid.UUID = Field(None)
    is_active: bool = True
    roles: list[Role] = Field(default_factory=lambda: [Role.USER])


class UserAddDTO(BaseModel):
    id: uuid.UUID
    firstname: Optional[str] = Field(None, max_length=100)
    lastname: Optional[str] = Field(None, max_length=100)
    phone: str = Field(min_length=1, max_length=20)
    hashed_password: str = Field(min_length=1, max_length=200)
    is_ready: Optional[int] = Field(None)
    group_id: uuid.UUID = Field(None)
    is_active: bool = True
    roles: list[Role] = Field(None)


class UserUpdateRequestDTO(BaseModel):
    firstname: Optional[str] = Field(None, max_length=100)
    lastname: Optional[str] = Field(None, max_length=100)
    phone: str = Field(min_length=1, max_length=20)
    is_ready: Optional[int] = Field(None)
    group_id: uuid.UUID = Field(None)
    is_active: bool = True
    roles: list[Role] = Field(default=None)


class UserPatchRequestDTO(BaseModel):
    firstname: Optional[str] = Field(None, max_length=100)
    lastname: Optional[str] = Field(None, max_length=100)
    phone: str = Field(min_length=1, max_length=20)
    is_ready: Optional[int] = Field(None)
    group_id: uuid.UUID = Field(None)
    is_active: bool = True
    roles: list[Role] = Field(None)


class UserRequestLoginDTO(BaseModel):
    phone: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=1, max_length=200)


class UserDTO(BaseModel):
    id: uuid.UUID
    firstname: Optional[str] = Field(None, max_length=100)
    lastname: Optional[str] = Field(None, max_length=100)
    avatar: Optional[str] = Field(None, max_length=200)
    phone: str = Field(min_length=1, max_length=20)
    is_ready: Optional[int] = Field(None)
    group_id: uuid.UUID = Field(None)
    is_active: bool = True
    roles: list[Role]

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(UserDTO):
    hashed_password: str = Field(min_length=1, max_length=200)


class UserRequestUpdatePasswordDTO(BaseModel):
    new_password: Optional[str] = Field(min_length=1, max_length=200)
    change_password: Optional[str] = Field(min_length=1, max_length=200)
