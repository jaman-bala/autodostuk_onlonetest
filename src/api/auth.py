import uuid

from fastapi import APIRouter, Response, Request
from uuid import UUID

from src.api.dependencies import UserIdDep, DBDep, RoleSuperuserDep
from src.exeptions import (
    UserNotFoundException,
    ObjectNotFoundException,
    UserNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    RolesAdminHTTPException,
    RolesSuperuserHTTPException,
    PhoneAlreadyExistsException,
    UserPhoneAlreadyExistsHTTPException,
    GroupsNotRegisterException,
    GroupNotRegisteredHTTPException,
)
from src.schemas.users import (
    UserRequestLoginDTO,
    UserRequestUpdatePasswordDTO,
    UserPatchRequestDTO,
    UserRequestAddDTO,
    UserResponseDTO,
)
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Authorization and authentication"])


@router.post("/create", summary="Creating a user 👨🏽‍💻")
async def register_user(
    role_superuser: RoleSuperuserDep,
    data: UserRequestAddDTO,
    db: DBDep,
):
    if not role_superuser:
        raise RolesSuperuserHTTPException
    try:
        users = await AuthService(db).register_user(data)
        users_response = UserResponseDTO(**users.model_dump())
    except PhoneAlreadyExistsException:
        raise UserPhoneAlreadyExistsHTTPException
    except GroupsNotRegisterException:
        raise GroupNotRegisteredHTTPException
    return {"message": "User created", "data": users_response}


@router.post("/login", summary="Login 👨🏽‍💻")
async def login_user(
    data: UserRequestLoginDTO,
    response: Response,
    db: DBDep,
):
    try:
        result = await AuthService(db).login_user(data, response)
        access_token = result["access_token"]
        last_login = result["last_login"]
    except UserNotFoundException:
        raise UserNotRegisteredHTTPException
    except PhoneAlreadyExistsException:
        raise UserPhoneAlreadyExistsHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    return {"message": "Success login", "access_token": access_token, "last_login": last_login}


@router.get("/me", summary="My profile👨🏽‍💻")
async def get_me(
    current_data: UserIdDep,
    db: DBDep,
):
    try:
        users = await AuthService(db).get_me(current_data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    return users


@router.get("/get_users_by_id/{user_id}", summary="Request by ID user")
async def get_users_by_id(
    role_admin: RoleSuperuserDep,
    user_id: uuid.UUID,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        users = await AuthService(db).get_by_users_id(user_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException
    return users


@router.get("/get_all_users", summary="Output of all users 👨🏽‍💻")
async def get_all_users(
    role_admin: RoleSuperuserDep,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        return await AuthService(db).get_all_users()
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException


@router.delete("/logout", summary="Logout 👨🏽‍💻")
async def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"message": "Logout success"}


@router.patch("/update/{user_id}", summary="Partial change 👨🏽‍💻")
async def update_user(
    user_id: UUID,
    role_admin: RoleSuperuserDep,
    db: DBDep,
    data: UserPatchRequestDTO,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        users = await AuthService(db).patch_user(user_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException
    return {"message": "User data has been partially changed", "data": users}


@router.delete("/{user_id}", summary="Deleting a user 👨🏽‍💻")
async def delete_user(user_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await AuthService(db).delete_user(user_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException
    return {"message": "User deleted"}


@router.put("/change_password/{user_id}", summary="Password reset")
async def change_password(
    user_id: UUID,
    role_admin: RoleSuperuserDep,
    data: UserRequestUpdatePasswordDTO,
    db: DBDep,
):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        await AuthService(db).change_password(user_id, data)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    return {"message": "Password successfully changed"}


@router.get("/get_users_by_group_id/{group_id}", summary="Displaying users by groups")
async def get_users_by_group_id(group_id: uuid.UUID, role_admin: RoleSuperuserDep, db: DBDep):
    if not role_admin:
        raise RolesAdminHTTPException
    try:
        users_by_groups = await AuthService(db).get_users_by_group_id(group_id)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundException
    return users_by_groups


@router.post("/refresh", summary="Refresh access_token using refresh_token")
async def refresh_access_token(
    request: Request,
    response: Response,
    db: DBDep,
):
    try:
        refresh_token = request.cookies.get("refresh_token")
        result = await AuthService(db).refresh_access_token(refresh_token, response)
        return {
            "status": "Token updated",
            "access_token": result["access_token"],
        }
    except ExpiredTokenHTTPException:
        raise ExpiredTokenHTTPException
    except UserNotFoundException:
        raise UserNotFoundException
