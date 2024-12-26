import uuid
from fastapi import APIRouter

from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    GroupsNotFoundException,
)
from src.schemas.group import GroupAddRequest, GroupPatch
from src.services.group import GroupsService

router = APIRouter(prefix="/group", tags=["Группы"])


@router.post("", summary="Создание группы")
async def create_group(
    data: GroupAddRequest,
  #  role_admin: RoleSuperuserDep,
    db: DBDep,
):
  #  if not role_admin:
   #     raise RolesAdminHTTPException
    groups = await GroupsService(db).create_group(data)
    return {"message": "Группа создан", "data": groups}


@router.get("", summary="Запрос всех групп")
async def get_group(
    current_data: UserIdDep,
    db: DBDep,
):
    try:
        group = await GroupsService(db).get_group()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise GroupsNotFoundException
    return {"message": "Запрос по ID", "data": group}


@router.get("/{group_id}", summary="Запрос по ID")
async def get_group_by_id(
    current_data: UserIdDep,
    group_id: uuid.UUID,
    db: DBDep,
):
    try:
        group = await GroupsService(db).get_by_group_id(group_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise GroupsNotFoundException
    return {"message": "Запрос по ID", "data": group}


@router.patch("/{group_id}", summary="Частичное изминение")
async def patch_group(
    grop_id: uuid.UUID, role_admin: RoleSuperuserDep, data: GroupPatch, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        group = await GroupsService(db).patch_group(grop_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise GroupsNotFoundException
    return {"message": "Данные честично изменены", "data": group}


@router.delete("/{group_id}", summary="Удаление данных")
async def delete_group(group_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await GroupsService(db).delete_group(group_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise GroupsNotFoundException
    return {"message": "Данные удалены"}
