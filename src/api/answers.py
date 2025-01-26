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
from src.schemas.answers import AnswerAddRequestDTO, AnswerPatchDTO, AnswerResponseDTO

router = APIRouter(prefix="/answers", tags=["Answers"])


@router.post("", summary="Adding a reply")
async def add_answers(
    role_admin: RoleSuperuserDep,
    db: DBDep,
    data: AnswerAddRequestDTO,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        answers = await AnswersService(db).create_answers(data)
        answers_response = AnswerResponseDTO(**answers.model_dump())
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"message": "Answer added", "data": answers_response}


@router.get("", summary="Request all data")
async def get_answers(current_data: UserIdDep, db: DBDep):
    try:
        answers = await AnswersService(db).get_answers()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return answers


@router.get("/{answer_id}", summary="Request by ID")
async def get_answer_by_id(answer_id: uuid.UUID, current_data: UserIdDep, db: DBDep):
    try:
        answers = await AnswersService(db).get_answer_id(answer_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return answers


@router.get("/by-question/{question_id}", summary="Get answers by question_id")
async def get_answers_by_question_id(question_id: uuid.UUID, current_data: UserIdDep, db: DBDep):
    try:
        answers = await AnswersService(db).get_answers_by_question_id(question_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return answers


@router.patch("/{answer_id}", summary="Partial change")
async def update_answer(
    answer_id: uuid.UUID, role_admin: RoleSuperuserDep, data: AnswerPatchDTO, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        answers = await AnswersService(db).patch_answers(answer_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"message": "The data has been honestly changed", "data": answers}


@router.delete("/{answer_id}", summary="Deleting a reply")
async def delete_answer(answer_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await AnswersService(db).delete_answer(answer_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise AnswersNotFoundException
    return {"message": "Data deleted"}
