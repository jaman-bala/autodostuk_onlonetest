import uuid
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.init import redis_manager
from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    TicketsNotFoundException,
)
from src.schemas.tickets import TicketAddRequestDTO, TicketPatchDTO, TicketResponseDTO
from src.services.tickets import TicketsService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("", summary="Add ticket")
async def create_tickets(
    role_admin: RoleSuperuserDep,
    db: DBDep,
    data: TicketAddRequestDTO,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        tickets = await TicketsService(db).create_tickets(data)
        await redis_manager.delete("tickets:get_all")
        tickets_response = TicketResponseDTO(**tickets.model_dump())
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TicketsNotFoundException
    return {"message": "Ticket created", "data": tickets_response}


@router.get("", summary="Request all data")
@cache(expire=300)
async def get_tickets(
    current_data: UserIdDep,
    db: DBDep,
):
    try:
        tickets = await TicketsService(db).get_tickets()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TicketsNotFoundException
    return tickets


@router.get("/{ticket_id}", summary="Request by ID")
@cache(expire=30)
async def get_tickets_by_id(current: UserIdDep, ticket_id: uuid.UUID, db: DBDep):
    try:
        tickets = await TicketsService(db).get_tickets_by_id(ticket_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TicketsNotFoundException
    return tickets


@router.patch("/{ticket_id}", summary="Partial data change")
async def patch_ticket(
    ticket_id: uuid.UUID, role_admin: RoleSuperuserDep, data: TicketPatchDTO, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        tickets = await TicketsService(db).patch_ticket(ticket_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TicketsNotFoundException
    return {"message": "Data partially changed", "data": tickets}


@router.delete("/{ticket_id}", summary="Deleted data")
async def delete_ticket(
    ticket_id: uuid.UUID,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await TicketsService(db).delete_ticket(ticket_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise TicketsNotFoundException
    return {"message": "Data deleted"}
