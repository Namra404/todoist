from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.tasks.dependencies import get_task_service
from src.api.tasks.exceptions import InsertTaskException, UpdateTaskException, GetTaskException, RemoveTaskException, \
    TaskNotFoundException
from src.api.tasks.schemas import TaskSchema, TaskCreate
from src.api.tasks.services import TaskService
from src.api.users.dependencies import get_user_by_jwt
from src.api.users.schemas import UserSchema

tasks_router = APIRouter()


@tasks_router.get('/')
async def get_tasks(
        # user: Annotated[UserSchema, Depends(get_user_by_jwt)],
        service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskSchema]:
    try:
        tasks = await service.get_all()
    except GetTaskException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return tasks


@tasks_router.get('/{task_id}')
async def receive_task(
        user: Annotated[UserSchema, Depends(get_user_by_jwt)],
        service: Annotated[TaskService, Depends(get_task_service)],
        task_id: UUID,
):
    try:
        task = await service.get(task_id=task_id)
    except GetTaskException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return task


@tasks_router.post('/', response_model=TaskSchema)
async def create_task(
        body: TaskCreate,
        service: TaskService = Depends(get_task_service),
) -> TaskSchema:
    # try:
    created_task = await service.create(body=body)
    # except InsertTaskException as e:
    #     raise HTTPException(status_code=404, detail=str(e))
    return created_task


@tasks_router.put('/{task_id}', response_model=TaskSchema)
async def update_task(
        task_id: UUID,
        body: TaskSchema,
        service: TaskService = Depends(get_task_service),
) -> TaskSchema:
    try:
        updated_task = await service.update(task_id, body=body)
    except UpdateTaskException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return updated_task


@tasks_router.delete('/{task_id}')
async def delete_task(
        task_id: UUID,
        service: TaskService = Depends(get_task_service),
):
    try:
        await service.remove(task_id=task_id)
    except GetTaskException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RemoveTaskException as e:
        raise HTTPException(status_code=404, detail=str(e))
