from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class AuthSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    name: str
    email: EmailStr


class TokenSchema(BaseModel):
    token: str
    token_type: str = "Bearer"


class AuthResponse(BaseModel):
    user: UserSchema
    token: TokenSchema
