from uuid import UUID

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str


class TaskSchema(TaskCreate):
    id: UUID
