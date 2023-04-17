import requests
api_key = '9cd207eb7d3a29cabb8960d43100ccdc'
# 60666/rows - Календарь маршрутов - работает ли маршрут сегодня? проверка bool
# 60664/rows - Маршруты  - код маршрута, номер и название
# 60662 - Остановки - код остановки и название 
# 60661 - Расписание рейсов - код остановки, номер остановки по номеру, время прибытия, код рейса
# 60665 - Рейсы маршрутов - код перечня дат, рейса и маршрута

url = f'https://apidata.mos.ru/v1/datasets/60664/rows?api_key={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for row in data:
        print(row["Cells"]["route_long_name"])
        
else:
    print('Failed to retrieve data from API')

