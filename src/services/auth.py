import jwt
import uuid
import logging

from uuid import UUID
from fastapi import Response
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

from src.config import settings
from src.exeptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    UserNotFoundException,
    IncorrectTokenHTTPException,
    IncorrectPasswordHTTPException,
    ExpiredTokenHTTPException,
    PhoneAlreadyExistsException,
    UserAlreadyHTTPException,
    GroupsNotRegisterException,
)
from src.models import UsersOrm
from src.schemas.users import (
    UserAdd,
    UserPatchRequest,
    UserRequestAdd,
    UserRequestLogin,
    UserRequestUpdatePassword,
)
from src.services.base import BaseService
from src.services.images import ImagesService

logger = logging.getLogger(__name__)


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, user: UsersOrm, response: Response) -> str:
        roles = [role.value for role in user.roles]
        data = {
            "user_id": str(user.id),
            "roles": roles,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        access_token = jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        # Устанавливаем токен в cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="None",
            secure=True,
        )

        return access_token

    def create_refresh_token(self, user: UsersOrm, response: Response) -> str:
        roles = [role.value for role in user.roles]
        data = {
            "user_id": str(user.id),
            "roles": roles,
            "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        }
        refresh_token = jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,  # Экспирация в днях
            samesite="None",
            secure=True,
        )

        return refresh_token

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenHTTPException
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenHTTPException

    async def register_user(self, data: UserRequestAdd):
        existing_user = await self.db.users.get_user_phone_number_with_hashed_password(
            phone=data.phone
        )
        if existing_user:
            raise PhoneAlreadyExistsException

        group = await self.db.users.get_user_group_id(group_id=data.group_id)
        if group:
            raise GroupsNotRegisterException

        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(
            id=uuid.uuid4(),
            firstname=data.firstname,
            lastname=data.lastname,
            phone=data.phone,
            hashed_password=hashed_password,
            is_ready=data.is_ready,
            group_id=data.group_id,
            is_active=True,
            roles=data.roles,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow(),
        )

        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
            return new_user_data
        except ObjectAlreadyExistsException as exc:
            raise UserAlreadyExistsException from exc

    async def get_me(self, user_id: UUID):
        try:
            user = await self.db.users.get_one_or_none(id=user_id)
            images_service = ImagesService(self.db)
            if not user:
                raise UserNotFoundException
            user_images = await images_service.get_all_images(user.id)
            if user_images:
                user.avatar = user_images[0]["avatar"]
            else:
                user.avatar = None
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenHTTPException
        return user

    async def get_by_users_id(self, user_id: uuid.UUID):
        try:
            users = await self.db.users.get_one_or_none(id=user_id)
        except UserNotFoundException:
            raise UserAlreadyHTTPException
        return users

    async def login_user(self, data: UserRequestLogin, response: Response):
        user = await self.db.users.get_user_phone_number_with_hashed_password(phone=data.phone)
        if not user:
            raise PhoneAlreadyExistsException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordHTTPException
        user.last_login = datetime.utcnow()
        await self.db.commit()
        access_token = self.create_access_token(user, response)
        self.create_refresh_token(user, response)
        return {
            "access_token": access_token,
            "user_id": str(user.id),
            "last_login": user.last_login,
        }

    async def refresh_access_token(self, refresh_token: str, response: Response) -> dict:
        try:
            payload = self.decode_access_token(refresh_token)
            user_id = payload.get("user_id")

            if not user_id:
                raise UserNotFoundException

            user = await self.db.users.get_one_or_none(id=user_id)
            if not user:
                raise UserNotFoundException
            access_token = self.create_access_token(user, response)
            return {
                "access_token": access_token,
            }
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenHTTPException
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenHTTPException

    async def get_all_users(self):
        try:
            users = await self.db.users.get_all()
            images_service = ImagesService(self.db)
            if not users:
                raise UserNotFoundException
            for user in users:
                user_images = await images_service.get_all_images(user.id)
                if user_images:
                    user.avatar = user_images[0]["avatar"]
                else:
                    user.avatar = None
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenHTTPException
        return users

    async def patch_user(self, user_id: UUID, data: UserPatchRequest, exclude_unset: bool = False):
        user = await self.db.users.get_one_or_none(id=user_id)
        if not user:
            raise UserNotFoundException
        await self.db.users.edit_patch(data, exclude_unset, id=user_id)
        await self.db.commit()
        return user

    async def change_password(self, user_id: UUID, data: UserRequestUpdatePassword):
        user = await self.db.users.get_one(id=user_id)
        if not user:
            raise UserNotFoundException
        hashed_new_password = self.hash_password(data.new_password)
        await self.db.users.update_user_hashed_password(user_id, hashed_new_password)
        await self.db.commit()

    async def delete_user(self, user_id: uuid.UUID):
        await self.db.users.delete(id=user_id)
        await self.db.commit()

    async def get_users_by_group_id(self, group_id: uuid.UUID):
        users = await self.db.users.get_users_by_group_id(group_id)
        return users
