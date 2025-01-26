import uuid
from fastapi import APIRouter

from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    TotalsNotFoundException,
)
from src.schemas.totals import TotalPatchDTO, TotalAddRequestDTO, TotalResponseDTO
from src.services.totals import TotalsService

router = APIRouter(prefix="/totals", tags=["Final report"])


@router.post("", summary="Adding a final report")
async def create_total(data: TotalAddRequestDTO, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        totals = await TotalsService(db).ctrate_totals(data)
        totals_response = TotalResponseDTO(**totals.model_dump())
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TotalsNotFoundException
    return {"message": "The final report has been created", "data": totals_response}


@router.get("", summary="Request all data")
async def get_total(current_data: UserIdDep, db: DBDep):
    try:
        totals = await TotalsService(db).get_totals()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TotalsNotFoundException
    return totals


@router.get("/{total_id}", summary="Request by ID")
async def get_totals_by_id(current: UserIdDep, total_id: uuid.UUID, db: DBDep):
    try:
        totals = TotalsService(db).get_totals_by_id(total_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TotalsNotFoundException
    return totals


@router.patch("/{total_id}", summary="Partial data change")
async def patch_total(
    total_id: uuid.UUID, role_admin: RoleSuperuserDep, data: TotalPatchDTO, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        totals = await TotalsService(db).patch_totals(total_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TotalsNotFoundException
    return {"message": "Data partially changed", "data": totals}


@router.delete("/{total_id}", summary="Deleting data")
async def delete_total(total_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await TotalsService(db).delete_totals(total_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TotalsNotFoundException
    return {"message": "Data deleted"}
