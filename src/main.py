from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.schedule import schedule_router


def get_application() -> FastAPI:
    application = FastAPI()

    origins = [
        "http://localhost:3001"
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(schedule_router)
    return application


app = get_application()
