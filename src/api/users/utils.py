from datetime import datetime

import bcrypt
import jwt

from src.core.config import JWT_KEY, JWT_ALGORITHM, JWT_EXPIRE_TIME
from src.api.users.schemas import TokenSchema, AuthResponse, UserSchema
from src.api.users.models import User
from src.api.users.serializers import UserSerializer


class PasswordHasher:
    @staticmethod
    async def encode(password: bytes) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt).decode()

    @staticmethod
    async def check(password: str, hashed_password: str) -> bool:
        if password is None or hashed_password is None:
            return False

        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password.encode()
        )


class JWTHasher:

    @staticmethod
    async def encode(user: UserSchema, key=JWT_KEY, algorithm=JWT_ALGORITHM) -> TokenSchema:
        now = datetime.utcnow()
        payload = {
            'sub': str(user.email),
            'iat': now,
            'exp': now + JWT_EXPIRE_TIME
        }

        token = jwt.encode(payload=payload, key=key, algorithm=algorithm)
        return TokenSchema(token=token, token_type="Bearer")

    @staticmethod
    async def decode(token: str, key=JWT_KEY, algorithm=JWT_ALGORITHM) -> dict:
        return jwt.decode(jwt=token, key=key, algorithms=[algorithm])


async def build_auth_response(user: User) -> AuthResponse:
    token = await JWTHasher.encode(user=user)
    return AuthResponse(
        user=UserSchema(name=user.name, email=user.email),
        token=token
    )