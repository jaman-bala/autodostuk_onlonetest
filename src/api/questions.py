import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, Form

from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    QuestionsNotFoundException,
)
from src.schemas.questions import QuestionPatchDTO, QuestionResponseDTO
from src.services.questions import QuestionsService

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/create", summary="Creating questions")
async def create_question(
    db: DBDep,
    role_admin: RoleSuperuserDep,
    title_ru: str = Form(None),
    title_kg: str = Form(None),
    description_ru: str = Form(None),
    description_kg: str = Form(None),
    ticket_id: uuid.UUID = Form(None),
    theme_id: uuid.UUID = Form(None),
    files: List[UploadFile] = File(None),
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        questions = await QuestionsService(db).create_questions(
            title_ru=title_ru,
            title_kg=title_kg,
            description_ru=description_ru,
            description_kg=description_kg,
            ticket_id=ticket_id,
            theme_id=theme_id,
            files=files,
        )
        questions_response = QuestionResponseDTO(**questions.model_dump())
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise QuestionsNotFoundException
    return {"message": "Question created", "data": questions_response}


@router.get("", summary="Request all questions")
async def get_questions(db: DBDep, current: UserIdDep):
    try:
        questions = await QuestionsService(db).get_questions()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise QuestionsNotFoundException
    return questions


@router.get("/{question_id", summary="Request by ID")
async def get_questions_by_id(current: UserIdDep, question_id: uuid.UUID, db: DBDep):
    try:
        questions = await QuestionsService(db).get_by_questions_id(question_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise QuestionsNotFoundException
    return questions


@router.get("/by-ticket/{ticket_id}", summary="Get questions by ticket_id")
async def get_questions_by_ticket_id(current: UserIdDep, ticket_id: uuid.UUID, db: DBDep):
    try:
        questions = await QuestionsService(db).get_questions_by_ticket_id(ticket_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise QuestionsNotFoundException
    return questions


@router.patch("/{question_id}", summary="Partial data change")
async def patch_question(
    question_id: uuid.UUID, role_admin: RoleSuperuserDep, data: QuestionPatchDTO, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        questions = await QuestionsService(db).patch_questions(question_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise QuestionsNotFoundException
    return {"message": "Data partially changed", "data": questions}


@router.delete("/{question_id}", summary="Delete a question")
async def delete_question(question_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await QuestionsService(db).delete_question(question_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise QuestionsNotFoundException
    return {"message": "Question deleted"}


@router.put("/{question_id}", summary="Updating files for a question")
async def put_question_files(
    db: DBDep,
    role_admin: RoleSuperuserDep,
    question_id: uuid.UUID,
    files: List[UploadFile] = File(None),
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        questions = await QuestionsService(db).patch_questions_file(question_id, files)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise QuestionsNotFoundException
    return {"message": "Files successfully updated", "data": questions}


@router.get("/random", summary="Output of 20 questions randomly")
async def get_random_question(db: DBDep):
    try:
        randoms = await QuestionsService(db).get_random_questions()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise QuestionsNotFoundException
    return randoms
