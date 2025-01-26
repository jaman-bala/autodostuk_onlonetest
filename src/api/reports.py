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
from src.schemas.reports import ReportAddRequestDTO, ReportPatchDTO, ReportResponseDTO
from src.services.reports import ReportsService

router = APIRouter(prefix="/reports", tags=["Report"])


@router.post("", summary="Adding a report")
async def create_report(
    data: ReportAddRequestDTO,
    current: UserIdDep,
    db: DBDep,
):
    try:
        reports = await ReportsService(db).create_reports(data)
        reports_response = ReportResponseDTO(**reports.model_dump())
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ReportsNotFoundException
    return {"message": "Report added", "data": reports_response}


@router.get("", summary="Request all data")
async def get_report(
    current: UserIdDep,
    db: DBDep,
):
    try:
        reports = await ReportsService(db).get_reports()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ReportsNotFoundException
    return reports


@router.get("/{report_id", summary="Request by ID")
async def get_reports_by_id(current: UserIdDep, report_id: uuid.UUID, db: DBDep):
    try:
        reports = await ReportsService(db).get_reports_by_id(report_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ReportsNotFoundException
    return reports


@router.patch("/{report_id}", summary="Partial change")
async def patch_report(
    report_id: uuid.UUID, role_admin: RoleSuperuserDep, data: ReportPatchDTO, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        reports = await ReportsService(db).patch_reports(report_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ReportsNotFoundException
    return {"message": "Data partially changed", "data": reports}


@router.delete("/{report_id}", summary="Deleting a report")
async def delete_report(report_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await ReportsService(db).delete_reports(report_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException
    return {"message": "Report deleted"}


@router.get("/get_reports_by_user_id/{user_id}", summary="Outputting a report on the user")
async def get_reports_by_user_id(
    current: UserIdDep,
    user_id: uuid.UUID,
    db: DBDep,
):
    try:
        reports_by_users = await ReportsService(db).get_reports_by_user_id(user_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException
    return reports_by_users
