from uuid import uuid4

from sqlalchemy import Column, UUID, String
from src.db.postgres import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String)
    name = Column(String)
    password = Column(String)


models = (
    User,
)
