from fastapi import FastAPI


from src.core.routes import get_main_router


class Server:
    def __init__(self):
        self.app = FastAPI()

    def init_routes(self):
        router = get_main_router()
        self.app.include_router(router)

    def run(self):
        self.init_routes()
        return self.app
