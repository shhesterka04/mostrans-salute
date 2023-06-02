import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json


def parse_schedule():
    url = 'https://transport.mos.ru/transport/schedule'

    options = Options()
    options.add_argument("--headless")

    service = Service(executable_path="src/mosru_api/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    data = []
    routes = soup.find_all('a', class_='ts-row')
    for route in routes:
        short_route_name_tag = route.find('div', class_='ts-number')
        long_route_name_tag = route.find('div', class_='ts-title')
        link = route.get('href')
        if short_route_name_tag and long_route_name_tag and link:
            data.append({
                'short_route_name': short_route_name_tag.text.strip(),
                'long_route_name': long_route_name_tag.text.strip().replace("\"", ""),
                'link': link,
            })

    driver.quit()

    return data


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
            hour_str = hour.find('div', class_='dt1').text.strip()[:-1]

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
