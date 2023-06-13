from fastapi import APIRouter
from starlette import status
from bson import json_util
import json

from src.mosru_api import parser
from src.core.database import routes
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
    # route_info = routes.find_one({"short_route_name": short_name})
    # if route_info is not None:
    #     return json.loads(json_util.dumps(route_info))
    # else:
    #     return {"error": "Route not found"}
    route_info = routes.find_one({"short_route_name": short_name})
    if route_info is not None:
        stops_data = json.loads(route_info['stops_data_0'])
        for stop in stops_data:
            if 'arrive_time' in stop:
                del stop['arrive_time']
        route_info['stops_data_0'] = stops_data
        stops_data = json.loads(route_info['stops_data_1'])
        for stop in stops_data:
            if 'arrive_time' in stop:
                del stop['arrive_time']
        route_info['stops_data_1'] = stops_data
        return json.loads(json_util.dumps(route_info))
    else:
        return {"error": "Route not found"}

@schedule_router.get(
    "/route_info_time",
    name="get_route_info_time",
    status_code=status.HTTP_200_OK
)
def get_route_info_with_time(short_name: str):
    """
    Возвращает ключевую информацию по искомому маршруту в json
    """
    route_info = routes.find_one({"short_route_name": short_name})
    if route_info is not None:
        return json.loads(json_util.dumps(route_info))
    else:
        return {"error": "Route not found"}

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
        if not routes.count_documents({"link": item['link']}):
            item["stops_data_0"] = parse_route(item['link'], direction=0)
            item["stops_data_1"] = parse_route(item['link'], direction=1)
            routes.insert_one(item)
            print(f"{item['short_route_name']} добавлен")
        else:
            print(f"{item['short_route_name']} уже есть")
