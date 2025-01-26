import uuid

from src.exeptions import TotalNotFoundException
from src.schemas.totals import TotalAddRequestDTO, TotalAddDTO, TotalPatchDTO
from src.services.base import BaseService


class TotalsService(BaseService):
    async def ctrate_totals(self, data: TotalAddRequestDTO):
        new_totals = TotalAddDTO(
            id=uuid.uuid4(),
            user_id=data.user_id,
            points=data.points,
            date_from=data.date_from,
            date_end=data.date_end,
        )
        await self.db.totals.add(new_totals)
        await self.db.commit()
        return new_totals

    async def get_totals(self):
        totals = await self.db.totals.get_all()
        return totals

    async def get_totals_by_id(self, total_id: uuid.UUID):
        totals = await self.db.totals.get_one_or_none(id=total_id)
        return totals

    async def patch_totals(
        self, total_id: uuid.UUID, data: TotalPatchDTO, exclude_unset: bool = False
    ):
        totals = await self.db.totals.get(total_id)
        if not totals:
            raise TotalNotFoundException
        await self.db.totals.edit_patch(data, exclude_unset=exclude_unset, id=total_id)
        await self.db.commit()
        return totals

    async def delete_totals(self, total_id: uuid.UUID):
        await self.db.totals.delete(id=total_id)
        await self.db.commit()
