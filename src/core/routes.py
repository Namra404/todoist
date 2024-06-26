from fastapi import APIRouter

from src.api.tasks.routes import tasks_router
from src.api.users.routes import user_router


def get_main_router():
    router = APIRouter(prefix='/v1/api')
    router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
    router.include_router(user_router, prefix="/users", tags=["User"])

    return router
