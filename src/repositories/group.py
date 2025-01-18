from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models import GroupOrm
from src.repositories.mappers.mappers import GroupDataMapper


class GroupsRepository(BaseRepository):
    model = GroupOrm
    mapper = GroupDataMapper

    async def get_group_one(self, title: str):
        query = select(self.model).filter_by(title=title)
        results = await self.session.execute(query)
        group = results.scalars().first()
        return group
