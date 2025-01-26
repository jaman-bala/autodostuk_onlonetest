import uuid
from fastapi import APIRouter

from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    PaymentsNotFoundException,
)
from src.schemas.payments import PaymentAddRequestDTO, PaymentPatchDTO, PaymentResponseDTO
from src.services.payments import PaymentsService

router = APIRouter(prefix="/payments", tags=["Payment"])


@router.post("", summary="Add payment")
async def create_payments(
    data: PaymentAddRequestDTO,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        payments = await PaymentsService(db).create_payments(data)
        payments_response = PaymentResponseDTO(**payments.model_dump())
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return {"message": "Payment created", "data": payments_response}


@router.get("", summary="Request all data")
async def get_payments(current: UserIdDep, db: DBDep):
    try:
        payments = await PaymentsService(db).get_payments()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return payments


@router.get("/{payment_id}", summary="Request by ID")
async def get_by_payments_id(
    current_data: UserIdDep,
    payment_id: uuid.UUID,
    db: DBDep,
):
    try:
        payments = await PaymentsService(db).get_payment_by_id(payment_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return payments


@router.patch("/{payment_id}", summary="Partial data change")
async def patch_payments(
    payment_id: uuid.UUID, role_admin: RoleSuperuserDep, data: PaymentPatchDTO, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        payments = await PaymentsService(db).patch_payments(payment_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return {"message": "Data partially changed", "data": payments}


@router.delete("/{payment_id}", summary="Deleting data")
async def delete_payments(payment_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await PaymentsService(db).delete_payments(payment_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return {"message": "Data deleted"}


@router.get("/by_users/{user_id}", summary="Receive payment by user")
async def get_payments_by_user_id(
    current: UserIdDep,
    user_id: uuid.UUID,
    db: DBDep,
):
    try:
        payments = await PaymentsService(db).get_payments_by_user_id(user_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return payments
