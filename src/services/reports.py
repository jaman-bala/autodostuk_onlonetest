import uuid

from src.exeptions import ReportNotFoundException
from src.schemas.reports import ReportAddRequestDTO, ReportAddDTO, ReportPatchDTO
from src.services.base import BaseService


class ReportsService(BaseService):
    async def create_reports(self, data: ReportAddRequestDTO):
        new_reports = ReportAddDTO(
            id=uuid.uuid4(),
            user_id=data.user_id,
            ticket_id=data.ticket_id,
            theme_id=data.theme_id,
            points=data.points,
            date_from=data.date_from,
            date_end=data.date_end,
        )
        await self.db.reports.add(new_reports)
        await self.db.commit()
        return new_reports

    async def get_reports(self):
        reports = await self.db.reports.get_all()
        return reports

    async def get_reports_by_id(self, report_id: uuid.UUID):
        reports = await self.db.reports.get_one_or_none(id=report_id)
        return reports

    async def patch_reports(
        self, report_id: uuid.UUID, data: ReportPatchDTO, exclude_unset: bool = False
    ):
        reports = await self.db.reports.get_one_or_none(id=report_id)
        if not reports:
            raise ReportNotFoundException
        await self.db.reports.edit_patch(data, exclude_unset=exclude_unset, id=report_id)
        await self.db.commit()
        return reports

    async def delete_reports(self, report_id: uuid.UUID):
        await self.db.reports.delete(id=report_id)
        await self.db.commit()

    async def get_reports_by_user_id(self, user_id: uuid.UUID):
        reports_by_users = await self.db.reports.get_reports_and_user_id(user_id)
        return reports_by_users
