from uuid import UUID

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession



from src.api.tasks.exceptions import TaskNotFound
from src.api.tasks.models import Tasks
from src.api.tasks.schemas import TaskSchema, TaskCreate


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, body: TaskCreate):

        task = Tasks(
            title=body.title,
            description=body.description,
            status=body.status,
            priority=body.priority
        )
        async with self.session.begin():
            self.session.add(task)
        return task

    async def get(self, task_id: UUID) -> Tasks:
        query = select(Tasks).filter_by(id=task_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()
        if task is None:
            raise TaskNotFound("Task not found")
        return task

    async def update(self, task_id: UUID, task_info: TaskSchema) -> Tasks:
        query = (
            update(Tasks)
            .filter_by(id=task_id)
            .values(
                title=task_info.title,
                description=task_info.description,
                status=task_info.status,
                priority=task_info.priority
            )
            .returning(Tasks)
        )
        async with self.session.begin():
            result = await self.session.execute(query)
            task = result.scalar_one_or_none()
        if task is None:
            raise TaskNotFound("Task not found")
        return task

    async def remove(self, task_id: UUID):
        query = delete(Tasks).filter_by(id=task_id)
        async with self.session.begin():
            await self.session.execute(query)

    async def get_all(self) -> list[Tasks]:
        query = select(Tasks)
        async with self.session.begin():
            result = await self.session.execute(query)
        return result.scalars().all()