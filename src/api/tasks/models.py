from uuid import uuid4

from sqlalchemy import Column, UUID, String
from src.db.postgres import Base


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)


models = (
    Tasks,
)
