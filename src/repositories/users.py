import uuid

from sqlalchemy import select, update
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_email_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)

    async def get_user_inn_with_hashed_password(self, inn: str):
        query = select(self.model).filter_by(inn=inn)
        results = await self.session.execute(query)
        model = results.scalars().one()
        return UserWithHashedPassword.model_validate(model)

    async def get_user_phone_number_with_hashed_password(self, phone: str):
        query = select(self.model).filter_by(phone=phone)
        result = await self.session.execute(query)
        model = result.scalars().first()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model.__dict__)

    async def get_user_group_id(self, group_id: uuid.UUID):
        query = select(self.model).filter_by(group_id=group_id)
        result = await self.session.execute(query)
        models = result.scalars().all()

        if not models:
            return None
        return models[0]

    async def get_user_none(self, phone: str):
        query = select(self.model).filter_by(phone=phone)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user

    async def update_user_hashed_password(self, user_id: int, hashed_password: str):
        query = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(hashed_password=hashed_password)
        )
        await self.session.execute(query)

    async def get_users_by_group_id(self, group_id: uuid.UUID):
        query = select(self.model).where(self.model.group_id == group_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_group_id_none(self, group_id: uuid.UUID):
        query = select(self.model).filter_by(group_id=group_id)
        result = await self.session.execute(query)
        group = result.scalars().first()
        return group
