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
    route_info = routes.find_one({"short_route_name": short_name})
    print(f"{short_name} найдено")
    if route_info is not None:
        print(f"1")
        route_info['stops_data'] = parse_route(route_info['link'])
        print(f"2")
        routes.update_one({'_id': route_info['_id']}, {'$set': route_info})
        print(f"3")
        return json.loads(json_util.dumps(route_info))
        print(f"4")
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
    # print("Данные получены")
    for item in data:
        if not routes.count_documents({"link": item['link']}):
            routes.insert_one(item)
            # print(f"Добавлено {item}")
