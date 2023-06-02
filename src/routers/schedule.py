from fastapi import APIRouter
from sqlalchemy import exists
from starlette import status
from src.core.database import session
from sqlalchemy import select
import json

from src.mosru_api import parser
from src.core.database import Route

schedule_router = APIRouter(
    prefix="/schedule",
    tags=["Schedule"]
)


@schedule_router.get(
    "/route_info",
    name="get_route_info",
    status_code=status.HTTP_200_OK
)
def get_route_info():
    """
    Возвращает ключевую информацию по искомому маршруту в json
    """
    short_name = "м16"
    stmt = select(Route).where(Route.short_route_name == short_name)
    result = session.execute(stmt)
    route_info = result.fetchone()

    if route_info is not None:
        return json.dumps(dict(route_info), ensure_ascii=False)
    else:
        return json.dumps({"error": "Route not found"}, ensure_ascii=False)
    # че то не понял


@schedule_router.get(
    "/stops",
    name="get_route_info",
    status_code=status.HTTP_200_OK
)
def get_stops_info(direction: int):
    """
    Возвращает все остановки маршрута и время остановок
    """
    pass


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
