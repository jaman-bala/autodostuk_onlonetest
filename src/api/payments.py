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
from src.schemas.payments import PaymentAddRequest, PaymentPatch, PaymentResponse
from src.services.payments import PaymentsService

router = APIRouter(prefix="/payments", tags=["Платёж"])


@router.post("", summary="Добавить платёж")
async def create_payments(
    data: PaymentAddRequest,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        payments = await PaymentsService(db).create_payments(data)
        payments_response = PaymentResponse(
            id=payments.id,
            user_id=payments.user_id,
            date_check=payments.date_check,
            price=payments.price,
        )
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return {"message": "Платёж создан", "data": payments_response}


@router.get("", summary="Запрос всех данных")
async def get_payments(current: UserIdDep, db: DBDep):
    try:
        payments = await PaymentsService(db).get_payments()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return payments


@router.get("/{payment_id}", summary="Запрос по ID")
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


@router.patch("/{payment_id}", summary="Частичное изминение данных")
async def patch_payments(
    payment_id: uuid.UUID, role_admin: RoleSuperuserDep, data: PaymentPatch, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        payments = await PaymentsService(db).patch_payments(payment_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return {"message": "Данные частично изменены", "data": payments}


@router.delete("/{payment_id}", summary="Удаление данных")
async def delete_payments(payment_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await PaymentsService(db).delete_payments(payment_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise PaymentsNotFoundException
    return {"message": "Данные удалены"}


@router.get("/by_users/{user_id}", summary="Получить платёж по пользователю")
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
