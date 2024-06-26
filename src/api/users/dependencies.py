from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import status
from jwt import InvalidTokenError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.exceptions import UserAuthException
from src.api.users.repository import UserRepository
from src.api.users.schemas import UserSchema
from src.api.users.serializers import UserSerializer
from src.api.users.services import UserService
from src.api.users.utils import JWTHasher
from src.db.postgres import get_db_session

http_bearer = HTTPBearer()


async def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]):
    repo = UserRepository(session)
    return UserService(repo)


async def get_payload_by_jwt(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> dict:
    token = credentials.credentials
    try:
        payload = await JWTHasher.decode(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}"
        )
    return payload


async def get_user_by_jwt(
        payload: Annotated[dict, Depends(get_payload_by_jwt)],
        service: Annotated[UserService, Depends(get_user_service)],
) -> UserSchema:
    """ Получение пользователя """

    email: EmailStr = payload.get("sub")

    try:
        user = await service.get_by_email(email)
    except UserAuthException:
        raise HTTPException(status_code=401, detail="Invalid JWT")

    return UserSerializer.serialize(user)
