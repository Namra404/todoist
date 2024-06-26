from typing import Iterable

from src.api.users.models import User
from src.api.users.schemas import UserSchema


class UserSerializer:
    @classmethod
    def serialize(cls, user: User | Iterable[User]) -> UserSchema | list[UserSchema]:
        if isinstance(user, Iterable):
            return [UserSchema.model_validate(u, from_attributes=True) for u in user]

        return UserSchema.model_validate(user, from_attributes=True)
