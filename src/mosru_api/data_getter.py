import requests

api_key = '9cd207eb7d3a29cabb8960d43100ccdc'
# 60664/rows - Маршруты  - код маршрута, номер и название - ОК
# 60665 - Рейсы маршрутов - код перечня дат, рейса и маршрута - 237 634 240000
# 60666/rows - Календарь маршрутов -
# 60661 - Расписание рейсов - код остановки, номер остановки по номеру, время прибытия, код рейса - 6_392_228 6_400_000
# 60662 - Остановки - код остановки и название 12440

url = 'https://apidata.mos.ru/v1/datasets/60664/rows'
params = {
    "api_key": api_key,
    "$filter": "Cells/route_short_name eq 'М16'",
}
response = requests.get(url=url, params=params)
if response.status_code == 200:
    data = response.json()
else:
    print('Failed to retrieve data from API')


# params = {
#     "api_key": api_key,
#     "$filter": f"Cells/route_id eq '{ans['route_id']}'",
#     "$top": 500,
#     "$skip": 0,
# }
