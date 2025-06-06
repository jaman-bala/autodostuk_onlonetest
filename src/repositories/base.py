from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound
from typing import Sequence
from fastapi import HTTPException
from pydantic import BaseModel

from src.exeptions import ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session
        if self.mapper is None:
            raise ValueError("Mapper not defined for repository")

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: Sequence[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def update(self, data: BaseModel, **filter_by) -> None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        qs = result.scalars().all()
        if not qs:
            raise HTTPException(status_code=404, detail="Object not found")

        if len(qs) > 1:
            raise HTTPException(status_code=422, detail="Several objects found")

        update_data_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(update_data_stmt)

    async def edit_patch(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        qs = result.scalars().all()
        if not qs:
            raise HTTPException(status_code=404, detail="Object not found")

        if len(qs) > 1:
            raise HTTPException(status_code=422, detail="Several objects found")

        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        qs = result.scalars().all()
        if not qs:
            raise HTTPException(status_code=404, detail="Object not found")

        if len(qs) > 1:
            raise HTTPException(status_code=422, detail="Several objects found")

        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
