from fastapi import APIRouter
from starlette import status

schedule_router = APIRouter(
    prefix="/schedule",
    tags=["Schedule"]
)


@schedule_router.get(
    "/{route_name}",
    name="get_route_info",
    status_code=status.HTTP_200_OK
)
def get_route_info(route_name: str):  # надо подумать над роут ид
    pass


@schedule_router.get(
    "/{route_name}/{stop_id}",
    name="get_stop_info",
    status_code=status.HTTP_200_OK
)
def get_stop_info(route_name: str, stop_id: int):  # надо подумать над стоп id
    pass


@schedule_router.get(
    "/",
    name="get_all_routes",
    status_code=status.HTTP_200_OK
)
def get_all_routes():
    pass
