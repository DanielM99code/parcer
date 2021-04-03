import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-volkswagen/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', 'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='page-item mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='proposition_link')

    cars = []
    for item in items:
        uah_price = item.find('span', class_='size16')
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'Цена отсутствует'
        cars.append({
               'title': item.find('h3', class_='proposition_name').get_text(strip=True),
               'usd_price': item.find('span', class_='green').get_text().replace('   ', ''),
               'uah_price': uah_price,
               'region': item.find('span', class_='item region').get_text()
            })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Маркаa', 'Цена в $', 'Цена в ГРН', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['usd_price'], item['uah_price'], item['region']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = get_pages_count(html.text)
        cars = []
        for page in range(1, pages_count +1):
            print(f'Загрузка {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
            save_file(cars, FILE)
        print(f'Полуено {len(cars)} автомобилей!')
        os.startfile(FILE)
    else:
        print('Error')


parse()
