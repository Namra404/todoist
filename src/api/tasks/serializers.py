from typing import Iterable

from src.api.tasks.models import Tasks
from src.api.tasks.schemas import TaskSchema


class TaskSerializer:
    @classmethod
    def serialize(cls, task: Tasks | Iterable[Tasks]) -> TaskSchema | list[TaskSchema]:
        if isinstance(task, Iterable):
            return [cls._serialize_single(item) for item in task]
        return cls._serialize_single(task)

    @classmethod
    def _serialize_single(cls, task: Tasks) -> TaskSchema:
        return TaskSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority
        )