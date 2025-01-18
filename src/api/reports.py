import uuid
from fastapi import APIRouter

from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    UserNotFoundException,
    ReportsNotFoundException,
)
from src.schemas.reports import ReportAddRequest, ReportPatch, ReportResponse
from src.services.reports import ReportsService

router = APIRouter(prefix="/reports", tags=["Отчёт"])


@router.post("", summary="Добавление отчёта")
async def create_report(
    data: ReportAddRequest,
    current: UserIdDep,
    db: DBDep,
):
    try:
        reports = await ReportsService(db).create_reports(data)
        reports_response = ReportResponse(
            id=reports.id,
            user_id=reports.user_id,
            ticket_id=reports.ticket_id,
            theme_id=reports.theme_id,
            points=reports.points,
            date_from=reports.date_from,
            date_end=reports.date_end,
        )
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ReportsNotFoundException
    return {"message": "Отчёт добавлен", "data": reports_response}


@router.get("", summary="Запрос всех данных")
async def get_report(
    current: UserIdDep,
    db: DBDep,
):
    reports = await ReportsService(db).get_reports()
    return reports


@router.get("/{report_id", summary="Запрос по ID")
async def get_reports_by_id(current: UserIdDep, report_id: uuid.UUID, db: DBDep):
    reports = await ReportsService(db).get_reports_by_id(report_id)
    return reports


@router.patch("/{report_id}", summary="Частичное изминение")
async def patch_report(
    report_id: uuid.UUID, role_admin: RoleSuperuserDep, data: ReportPatch, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        reports = await ReportsService(db).patch_reports(report_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ReportsNotFoundException
    return {"message": "Данные частично изменены", "data": reports}


@router.delete("/{report_id}", summary="Удаление отчёта")
async def delete_report(report_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await ReportsService(db).delete_reports(report_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException
    return {"message": "Отчёт удален"}


@router.get("/get_reports_by_user_id/{user_id}", summary="Вывод отчёта по пользователю")
async def get_reports_by_user_id(
    current: UserIdDep,
    user_id: uuid.UUID,
    db: DBDep,
):
    try:
        reports = await ReportsService(db).get_reports_by_user_id(user_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException
    return reports
