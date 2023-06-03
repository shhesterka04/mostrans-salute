import sqlalchemy
from fastapi import APIRouter
from sqlalchemy import exists
from starlette import status
from src.core.database import session
from sqlalchemy import select
import json

from src.mosru_api import parser
from src.core.database import Route
from src.mosru_api.parser import parse_route

schedule_router = APIRouter(
    prefix="/schedule",
    tags=["Schedule"]
)


@schedule_router.get(
    "/route_info",
    name="get_route_info",
    status_code=status.HTTP_200_OK
)
def get_route_info(short_name: str):
    """
    Возвращает ключевую информацию по искомому маршруту в json
    """
    query = select(Route).where(Route.short_route_name == short_name)
    result = session.execute(query)
    route_info = result.scalars().first()

    if route_info is not None:
        return route_info
    else:
        return {"error": "Route not found"}


@schedule_router.get(
    "/stops",
    name="get_route_info",
    status_code=status.HTTP_200_OK
)
def get_stops_info(direction: int = 0, url :str):
    """
    Возвращает все остановки маршрута и время остановок
    """

    data = parse_route(direction, url=url)
    return data



@schedule_router.post(
    "/update_data",
    name="update_routes_data",
    status_code=status.HTTP_200_OK
)
def update_routes_data():
    """
    Берет данные с главной страницы транспорта mos.ru со ссылками на маршруты и добавляет их в таблицу
    """
    data = parser.parse_schedule()
    for item in data:
        if not session.query(exists().where(Route.link == item['link'])).scalar():
            route = Route(item['short_route_name'], item['long_route_name'], item['link'])
            session.add(route)
    session.commit()

# @schedule_router.post(
#     "update_stops_info",
#     name="update_stops_info",
#     status_code=status.HTTP_200_OK
# )
# def update_stops_info():
#     """
#     Берет данные по конкретному маршруту и кеширует остановки и время остановок
#     """
#     pass
