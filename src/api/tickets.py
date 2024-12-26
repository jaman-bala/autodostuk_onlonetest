import uuid
from fastapi import APIRouter

from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    TicketsNotFoundException,
)
from src.schemas.tickets import TicketAddRequest, TicketPatch
from src.services.tickets import TicketsService

router = APIRouter(prefix="/tickets", tags=["Билеты"])


@router.post("", summary="Добавить билет")
async def create_tickets(
    data: TicketAddRequest,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    tickets = await TicketsService(db).create_tickets(data)
    return {"message": "Билет создан", "data": tickets}


@router.get("", summary="Запрос всех данных")
async def get_tickets(current_data: UserIdDep, db: DBDep):
    return await TicketsService(db).get_tickets()


@router.get("/{ticket_id}", summary="Запрос по ID")
async def get_tickets_by_id(current: UserIdDep, ticket_id: uuid.UUID, db: DBDep):
    await TicketsService(db).get_tickets_by_id(ticket_id)


@router.patch("/{ticket_id}", summary="Частичное изминение данных")
async def patch_ticket(
    ticket_id: uuid.UUID, role_admin: RoleSuperuserDep, data: TicketPatch, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        tickets = await TicketsService(db).patch_ticket(ticket_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TicketsNotFoundException
    return {"message": "Данные частично изменены", "data": tickets}


@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await TicketsService(db).delete_ticket(ticket_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TicketsNotFoundException
    return {"message": "Билет удален"}
