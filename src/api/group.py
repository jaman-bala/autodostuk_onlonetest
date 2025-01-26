import uuid
from fastapi import APIRouter

from src.api.dependencies import DBDep, RoleSuperuserDep, UserIdDep
from src.exeptions import (
    RolesAdminHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    ObjectNotFoundException,
    GroupNotFoundException,
    GroupHTTPException,
)
from src.schemas.group import GroupAddRequestDTO, GroupPatchDTO, GroupResponseDTO
from src.services.group import GroupsService

router = APIRouter(prefix="/group", tags=["Groups"])


@router.post("", summary="Create a group")
async def create_group(
    data: GroupAddRequestDTO,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        groups = await GroupsService(db).create_group(data)
        groups_response = GroupResponseDTO(**groups.model_dump())
    except GroupNotFoundException:
        raise GroupHTTPException
    return {"message": "Group created", "data": groups_response}


@router.get("", summary="Query all groups")
async def get_group(
    current_data: UserIdDep,
    db: DBDep,
):
    try:
        groups = await GroupsService(db).get_group()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise GroupHTTPException
    return groups


@router.get("/{group_id}", summary="Request by ID")
async def get_group_by_id(
    current_data: UserIdDep,
    group_id: uuid.UUID,
    db: DBDep,
):
    try:
        groups = await GroupsService(db).get_by_group_id(group_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise GroupHTTPException
    return groups


@router.patch("/{group_id}", summary="Partial change")
async def patch_group(
    grop_id: uuid.UUID, role_admin: RoleSuperuserDep, data: GroupPatchDTO, db: DBDep
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        groups = await GroupsService(db).patch_group(grop_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise GroupHTTPException
    return {"message": "The data has been honestly changed", "data": groups}


@router.delete("/{group_id}", summary="Deleting data")
async def delete_group(
    group_id: uuid.UUID,
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await GroupsService(db).delete_group(group_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise GroupHTTPException
    return {"message": "Data deleted"}
