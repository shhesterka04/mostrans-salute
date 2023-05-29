import requests
from src.core.config import API_KEY
import timeit


def get_response(dataset):
    data = []
    url = f"https://apidata-new.mos.ru/v1/datasets/{dataset}/count"
    params = {
        "api_key": API_KEY,
    }
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        length = int(response.json())
    else:
        print(f"Response text: {response.text}")
    for skip in range(0, length, 500):
        top = 500
        url = f"https://apidata-new.mos.ru/v1/datasets/{dataset}/rows"
        params = {
            "api_key": API_KEY,
            "$top": top,
            "$skip": skip
        }
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            data.append(response.json())
        else:
            print('Failed to retrieve data from API')
            print(f"Response text: {response.text}")
    return data


def get_id_routes():
    data = get_response(60664)
    for row in data:
        route_short_name = row["Cells"]["route_short_name"]
        route_short_name = row["Cells"]["route_short_name"]
        route_id = row["Cells"]["route_id"]
        route_long_name = row["Cells"]["route_long_name"]
        route_type = row["Cells"]["route_type"]


def get_trip_id():
    data = get_response(60665)
    for row in data:
        date_interval = row["Cells"]["service_id"]
        trip_id = row["Cells"]["trip_id"]
        direction_id = row["Cells"]["direction_id"]
        route_id = row["Cells"]["route_id"]


def get_time_and_stops_id():
    data = get_response(60661)
    for row in data:
        trip_id = row["Cells"]["trip_id"]
        arrival_time = row["Cells"]["arrival_time"]
        stop_id = row["Cells"]["stop_id"]
        trip_id = row["Cells"]["trip_id"]
        stop_sequence = row["Cells"]["stop_sequence"]


def get_stops_names():
    data = get_response(60662)
    for row in data:
        stop_id = row["Cells"]["stop_id"]
        stop_name = row["Cells"]["stop_name"]


def get_cal_routes():
    data = get_response(60666)
    for row in data:
        service_id = row["Cells"]["service_id"]
        start_date = row["Cells"]["start_date"]
        end_date = row["Cells"]["end_date"]
        monday = row["Cells"]["monday"]
        tuesday = row["Cells"]["tuesday"]
        wednesday = row["Cells"]["wednesday"]
        thursday = row["Cells"]["thursday"]
        friday = row["Cells"]["friday"]
        saturday = row["Cells"]["saturday"]
        sunday = row["Cells"]["sunday"]


start = timeit.default_timer()
get_id_routes()
get_trip_id()
get_time_and_stops_id()
get_stops_names()
get_cal_routes()
end = timeit.default_timer()

print(f"Time taken is {end - start}s")