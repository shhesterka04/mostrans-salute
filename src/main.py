from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(schedule_router)
