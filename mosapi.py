import requests
api_key = '9cd207eb7d3a29cabb8960d43100ccdc'
# 60664/rows - Маршруты  - код маршрута, номер и название - ОК
# 60665 - Рейсы маршрутов - код перечня дат, рейса и маршрута - 237 634 240000
# 60666/rows - Календарь маршрутов - 
# 60661 - Расписание рейсов - код остановки, номер остановки по номеру, время прибытия, код рейса - 6_392_228 6_400_000

# 60662 - Остановки - код остановки и название 12440



ans = {
    "route_short_name": "", 
    "route_long_name": "",
    "route_type": -1, 
    "route_id": -1,
    "trips": {
    },
    "workdays": {
        'monday': -1,
        'tuesday': -1,
        'wednesday': -1,
        'thursday': -1,
        'friday': -1,
        'saturday': -1,
        'sunday': -1,
    },
    "start_date": "",
    "end_date": "",
}


url = 'https://apidata.mos.ru/v1/datasets/60664/rows'
params = {
    "api_key": api_key,
    "$filter": "Cells/route_short_name eq 'М16'",
}
response = requests.get(url=url, params=params)
if response.status_code == 200: 
    data = response.json()
    for row in data:
            ans["route_short_name"] = row["Cells"]["route_short_name"]
            ans["route_long_name"] = row["Cells"]["route_long_name"]
            ans["route_type"] = row["Cells"]["route_type"]
            ans["route_id"] = row["Cells"]["route_id"]
else:
    print('Failed to retrieve data from API')


url = "https://apidata.mos.ru/v1/datasets/60665/rows/"
params = {
    "api_key": api_key,
    "$filter": f"Cells/route_id eq '{ans['route_id']}'",
    "$top": 500,
    "$skip": 0,
}
response = requests.get(url=url, params=params)
if response.status_code == 200:
    data = response.json()
    for row in data:
        key = row["Cells"]["trip_id"]
        ans["trips"][key] = {row["Cells"]["trip_id"]: {"service_id": row["Cells"]["service_id"], "direction_id": row["Cells"]["direction_id"], "stops": {}, "workdays": {}, start_date}}
else:
    print('Failed to retrieve data from API')

# url = f"https://apidata.mos.ru/v1/datasets/60666/rows?&api_key={api_key}"
# response = requests.get(url)
# if response.status_code == 200:
#     data = response.json()
#     print(skip)
#     for row in data:
#         if row["Cells"]["service_id"] == ans["service_id"]:
#             ans["workdays"]["monday"] = row["Cells"]["monday"]
#             ans["workdays"]["tuesday"] = row["Cells"]["tuesday"]
#             ans["workdays"]["wednesday"] = row["Cells"]["wednesday"]
#             ans["workdays"]["thursday"] = row["Cells"]["thursday"]
#             ans["workdays"]["friday"] = row["Cells"]["friday"]
#             ans["workdays"]["saturday"] = row["Cells"]["saturday"]
#             ans["workdays"]["sunday"] = row["Cells"]["sunday"]
#             ans["start_date"] = row["Cells"]["start_date"]
#             ans["end_date"] = row["Cells"]["end_date"]
#         else:
#             print('Failed to retrieve data from API')

# for skip in range(0,6_400_000,10_000):
#     print(skip)
#     url = f'https://apidata.mos.ru/v1/datasets/60661/rows?skip={skip}&$top=10000&$orderby="stop_sequence desc"&api_key={api_key}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         for row in data:
#             if row["Cells"]["trip_id"] == ans["trip_id"]:
#                 ans["stops"]["stop_id"] = row["Cells"]["stop_id"]
#                 ans["stops"]["arrival_time"] = row["Cells"]["arrival_time"]
#                 ans["stops"]["stop_sequence"] = row["Cells"]["stop_sequence"]
#     else:
#         print('Failed to retrieve data from API')

# print("61 ok")

# url = f"https://apidata.mos.ru/v1/datasets/60662/rows?$top=10&api_key={api_key}"
# response = requests.get(url)
# if response.status_code == 200:
#     data = response.json()
#     for row in data:
#         if row["Cells"]["stop_id"] == ans["stops"]["stop_id"]:
#             ans["stops"]["stop_name"] = row["Cells"]["stop_name"]
# else:
#     print('Failed to retrieve data from API')

# print("62 ok")

# print(ans)


#---------------------

# url = f'https://apidata.mos.ru/v1/datasets/60661/rows?$top=30&$orderby="stop_sequence desc"&api_key={api_key}'
# params = {
#     "api_key": api_key,
#     "$filter": f"Cells/route_id eq '{ans['route_id']}'",
#     "$top": 500,
# }
# response = requests.get(url)
# if response.status_code == 200:
#     data = response.json()
#     for row in data:
#         print(row['Cells'])
# else:
#     print('Failed to retrieve data from API')