import uuid

from src.exeptions import GroupNotFoundException
from src.schemas.group import GroupAddRequestDTO, GroupAddDTO, GroupPatchDTO
from src.services.base import BaseService


class GroupsService(BaseService):
    async def create_group(self, data: GroupAddRequestDTO):
        groups = await self.db.groups.get_group_one(title=data.title)
        if groups:
            raise GroupNotFoundException
        new_groups = GroupAddDTO(
            id=uuid.uuid4(),
            title=data.title,
            category=data.category,
            user_quantity=data.user_quantity,
            date_from=data.date_from,
            date_end=data.date_end,
            period=data.period,
            is_active=True,
        )
        await self.db.groups.add(new_groups)
        await self.db.commit()
        return new_groups

    async def get_group(self):
        groups = await self.db.groups.get_all()
        return groups

    async def get_by_group_id(self, group_id: uuid.UUID):
        group_by_id = await self.db.groups.get_one_or_none(id=group_id)
        return group_by_id

    async def patch_group(
        self, group_id: uuid.UUID, data: GroupPatchDTO, exclude_unset: bool = False
    ):
        groups = await self.db.groups.get_one_or_none(id=group_id)
        if not groups:
            raise GroupNotFoundException
        await self.db.groups.edit_patch(data, exclude_unset=exclude_unset, id=group_id)
        await self.db.commit()
        return groups

    async def delete_group(self, group_id: uuid.UUID):
        await self.db.groups.delete(id=group_id)
        await self.db.commit()
