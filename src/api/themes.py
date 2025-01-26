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
from src.schemas.themes import ThemeAddRequestDTO, ThemePatchDTO, ThemeResponseDTO
from src.services.themes import ThemesService

router = APIRouter(prefix="/themes", tags=["Themes"])


@router.post("", summary="Create a theme")
async def create_theme(
    data: ThemeAddRequestDTO,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        themes = await ThemesService(db).create_themes(data)
        themes_response = ThemeResponseDTO(**themes.model_dump())
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    return {"message": "theme created", "data": themes_response}


@router.get("", summary="Request all theme")
async def get_theme(
    current_data: UserIdDep,
    db: DBDep,
):
    try:
        themes = await ThemesService(db).get_theme()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    return themes


@router.get("/{theme_id}", summary="Request by ID")
async def get_themes_by_id(current: UserIdDep, theme_id: uuid.UUID, db: DBDep):
    try:
        themes = ThemesService(db).get_themes_by_id(theme_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    return themes


@router.patch("/{theme_id}", summary="Partial data change")
async def patch_theme(
    theme_id: uuid.UUID, role_admin: RoleSuperuserDep, data: ThemePatchDTO, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        themes = await ThemesService(db).patch_theme(theme_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ThemesNotFoundException
    return {"message": "Data partially changed", "data": themes}


@router.delete("/{theme_id}", summary="Deleting data")
async def delete_theme(theme_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await ThemesService(db).delete_theme(theme_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise ThemesNotFoundException
    return {"message": "Data deleted"}
