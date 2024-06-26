from pydantic import EmailStr

from src.api.users.exceptions import UserAuthException
from src.api.users.repository import UserRepository
from src.api.users.schemas import RegisterSchema, AuthResponse, AuthSchema
from src.api.users.utils import build_auth_response, PasswordHasher


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, body: RegisterSchema) -> AuthResponse:
        if await self.repo.email_exists(body.email):
            raise UserAuthException('User already exists!')

        user = await self.repo.create(body)
        return await build_auth_response(user=user)

    async def authenticate(self, body: AuthSchema) -> AuthResponse:
        user = await self.repo.get_by_email(body.email)
        if not user or not await PasswordHasher.check(body.password, user.password):
            raise UserAuthException('Invalid email or password')

        return await build_auth_response(user=user)

    async def get_by_email(self, email: EmailStr):
        user = await self.repo.get_by_email(email)
        if not user:
            raise UserAuthException('Invalid email or password')
        return user
