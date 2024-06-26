from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.models import User
from src.api.users.schemas import RegisterSchema
from src.api.users.utils import PasswordHasher


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def email_exists(self, email: EmailStr) -> bool:
        query = select(User).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def create(self, user: RegisterSchema) -> User:
        password = await PasswordHasher.encode(user.password.encode())
        db_user = User(
            name=user.name,
            email=user.email,
            password=password
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get_by_email(self, email: EmailStr) -> User:
        query = select(User).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()