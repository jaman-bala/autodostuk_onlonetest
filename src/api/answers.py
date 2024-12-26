import uuid
from fastapi import APIRouter

from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    AnswersNotFoundException,
)
from src.services.answers import AnswersService
from src.schemas.answers import AnswerAddRequest, AnswerPatch

router = APIRouter(prefix="/answers", tags=["Ответы"])


@router.post("", summary="Добавление ответа")
async def add_answers(
    data: AnswerAddRequest,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        answers = await AnswersService(db).create_answers(data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"status": "Ответ добавлен", "data": answers}


@router.get("", summary="Запрос всех данных")
async def get_answers(current_data: UserIdDep, db: DBDep):
    try:
        answers = await AnswersService(db).get_answers()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"status": "Запрос всех данных", "data": answers}


@router.get("/{answer_id}", summary="Запрос по ID")
async def get_answer_by_id(answer_id: uuid.UUID, current_data: UserIdDep, db: DBDep):
    try:
        answers = await AnswersService(db).get_answer_id(answer_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"status": "Запрос по ID", "data": answers}


@router.get("/by-question/{question_id}", summary="Получить ответы по question_id")
async def get_answers_by_question_id(question_id: uuid.UUID, current_data: UserIdDep, db: DBDep):
    try:
        answers = await AnswersService(db).get_answers_by_question_id(question_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"status": "Получить ответы по question_id", "data": answers}


@router.patch("/{answer_id}", summary="Частичное изминение")
async def update_answer(
    answer_id: uuid.UUID, role_admin: RoleSuperuserDep, data: AnswerPatch, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        answers = await AnswersService(db).patch_answers(answer_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"message": "Данные честично изменены", "data": answers}


@router.delete("/{answer_id}", summary="Удаление ответа")
async def delete_answer(answer_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await AnswersService(db).delete_answer(answer_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"message": "Данные удалены"}
