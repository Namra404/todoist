from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.tasks.repository import TaskRepository
from src.api.tasks.services import TaskService
from src.db.postgres import get_db_session


async def get_task_service(session: Annotated[AsyncSession, Depends(get_db_session)]):
    repo = TaskRepository(session)
    return TaskService(repo)
