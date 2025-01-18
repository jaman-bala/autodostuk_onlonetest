import uuid
from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep, RoleSuperuserDep
from src.exeptions import (
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    RolesAdminHTTPException,
    ObjectNotFoundException,
    ThemesNotFoundException,
)
from src.schemas.themes import ThemeAddRequest, ThemePatch, ThemeResponse
from src.services.themes import ThemesService

router = APIRouter(prefix="/themes", tags=["Тема"])


@router.post("", summary="Создание темы")
async def create_theme(
    data: ThemeAddRequest,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    themes = await ThemesService(db).create_themes(data)
    themes_response = ThemeResponse(
        id=themes.id,
        title_ru=themes.title_ru,
        title_kg=themes.title_kg,
    )
    return {"message": "Тема создана", "data": themes_response}


@router.get("", summary="Запрос всех тем")
async def get_theme(
    current_data: UserIdDep,
    db: DBDep,
):
    try:
        themes = await ThemesService(db).get_theme()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    return themes


@router.get("/{theme_id}", summary="Запрос по ID")
async def get_themes_by_id(current: UserIdDep, theme_id: uuid.UUID, db: DBDep):
    try:
        themes = ThemesService(db).get_themes_by_id(theme_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    return themes


@router.patch("/{theme_id}", summary="Частичное изминение данных")
async def patch_theme(
    theme_id: uuid.UUID, role_admin: RoleSuperuserDep, data: ThemePatch, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        themes = await ThemesService(db).patch_theme(theme_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ThemesNotFoundException
    return {"message": "Данные частично изменены", "data": themes}


@router.delete("/{theme_id}", summary="Удаление данных")
async def delete_theme(theme_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await ThemesService(db).delete_theme(theme_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ThemesNotFoundException
    return {"message": "Данные удалены"}
