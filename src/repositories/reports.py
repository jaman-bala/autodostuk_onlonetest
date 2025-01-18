import uuid
from sqlalchemy import select

from src.models.reports import ReportOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ReportDataMapper


class ReportsRepository(BaseRepository):
    model = ReportOrm
    mapper = ReportDataMapper

    async def get_reports_and_user_id(self, user_id: uuid.UUID):
        query = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
