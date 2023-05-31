import requests
from bs4 import BeautifulSoup
import timeit
import asyncio
from pyppeteer import launch
import json


async def parse_schedule():
    url = 'https://transport.mos.ru/transport/schedule'

    # Запуск браузера
    browser = await launch()
    # Открытие новой вкладки
    page = await browser.newPage()
    # Переход на страницу
    await page.goto(url)

    data = []
    routes = await page.querySelectorAll('a.ts-row')
    for route in routes:
        short_route_name = await page.evaluate('(element) => element.textContent',
                                               await route.querySelector('div.ts-number'))
        long_route_name = await page.evaluate('(element) => element.textContent',
                                              await route.querySelector('div.ts-title'))
        link = route.getProperty('href')

        if short_route_name and long_route_name and link:
            data.append({
                'short_route_name': short_route_name,
                'long_route_name': long_route_name,
                'link': link,
            })

    await browser.close()
    return json.dumps(data, ensure_ascii=False, indent=4)




def parse_route(url, direction=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []

    stops = soup.find_all('li', {'data-direction': str(direction)})

    for stop in stops:
        stop_name = stop.find('div', class_='a_dotted d-inline').text.strip()

        hours = stop.find_all('div', class_='raspisanie_data')

        arrive_time = {}
        for hour in hours:
            hour_str = hour.find('div', class_='dt1').text.strip()[:-1]  # убираем ':' из строки часа

            if not hour_str:
                continue

            minutes_tags = hour.find_all('div', class_='div10')
            minutes = [minute.text.strip() for minute in minutes_tags]

            arrive_time[hour_str] = minutes

        data.append({
            "stop_name": stop_name,
            'arrive_time': arrive_time,
        })

    return json.dumps(data, ensure_ascii=False, indent=4)


start = timeit.default_timer()
print(asyncio.run(parse_schedule()))
# print(parse_route("https://transport.mos.ru/transport/schedule/route/2111"))
end = timeit.default_timer()
