from uuid import UUID

from src.api.tasks.exceptions import InsertTaskException, UpdateTaskException, GetTaskException, RemoveTaskException, \
    TaskNotFoundException
from src.api.tasks.repository import TaskRepository
from src.api.tasks.schemas import TaskSchema, TaskCreate
from src.api.tasks.serializers import TaskSerializer


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create(self, body: TaskCreate) -> TaskSchema:
        try:
            task = await self.repo.create(body=body)
            return TaskSerializer.serialize(task)
        except Exception as e:
            raise InsertTaskException(str(e))

    async def update(self, task_id: UUID, body: TaskSchema) -> TaskSchema:
        try:
            task = await self.repo.update(task_id, body)
            return TaskSerializer.serialize(task)
        except Exception as e:
            raise UpdateTaskException(str(e))

    async def remove(self, task_id: UUID):
        task = await self.get(task_id=task_id)

        if not task:
            raise TaskNotFoundException('Order not found')

        try:
            await self.repo.remove(task_id)
        except Exception as e:
            raise RemoveTaskException(str(e))

    async def get(self, task_id: UUID) -> TaskSchema:
        try:
            task = await self.repo.get(task_id)
            return TaskSerializer.serialize(task)
        except Exception as e:
            raise GetTaskException(str(e))

    async def get_all(self) -> list[TaskSchema]:
        try:
            tasks = await self.repo.get_all()
            return TaskSerializer.serialize(tasks)
        except Exception as e:
            raise GetTaskException(str(e))
