import requests
api_key = '9cd207eb7d3a29cabb8960d43100ccdc'
# 60664/rows - Маршруты  - код маршрута, номер и название
# 60666/rows - Календарь маршрутов - работает ли маршрут сегодня? проверка bool

# 60662 - Остановки - код остановки и название 12440
# 60661 - Расписание рейсов - код остановки, номер остановки по номеру, время прибытия, код рейса - 6392228
# 60665 - Рейсы маршрутов - код перечня дат, рейса и маршрута - 237634

# url = f'https://apidata.mos.ru/v1/datasets/60664/rows?api_key={api_key}'

# response = requests.get(url)

# ans = {
#     "route_short_name": "",
#     "route_long_name": "",
#     "route_type": -1,
#     "route_id": -1,
# }

# if response.status_code == 200:
#     data = response.json()
#     for row in data:
#         if row["Cells"]["route_short_name"] == "М16":
#             ans["route_short_name"] = "M16"
#             ans["route_long_name"] = row["Cells"]["route_long_name"]
#             ans["route_type"] = row["Cells"]["route_type"]
#             ans["route_id"] = row["Cells"]["route_id"]

# else:
#     print('Failed to retrieve data from API')

url = f'https://apidata.mos.ru/v1/datasets/60666/count?api_key={api_key}'
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data)
        # if row["Cells"]["route_id"] == ans["route_id"]:
        #print(row["Cells"])
else:
    print('Failed to retrieve data from API')


