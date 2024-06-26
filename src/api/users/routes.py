from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.users.dependencies import get_user_service
from src.api.users.exceptions import UserAuthException
from src.api.users.schemas import RegisterSchema, AuthResponse, AuthSchema
from src.api.users.services import UserService

user_router = APIRouter()


@user_router.post('/register', response_model=AuthResponse)
async def register_user(
        body: RegisterSchema,
        service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        response = await service.register(body)
    except UserAuthException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@user_router.post('/login', response_model=AuthResponse)
async def authenticate_user(
        body: AuthSchema,
        service: Annotated[UserService, Depends(get_user_service)]
) -> AuthResponse:
    try:
        response = await service.authenticate(body)
    except UserAuthException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response
