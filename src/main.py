from fastapi import FastAPI

from src.routers.schedule import schedule_router


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(schedule_router)
    return application


app = get_application()
