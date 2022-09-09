import time
from datetime import datetime
import re
from math import ceil
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from peewee import *
import asyncio
import aiohttp

db = PostgresqlDatabase(database='postgres', user='postgres', password='postgres', host='db')


class Info(Model):
    image_src = CharField(null=True)
    title = TextField()
    date = DateField(formats=["%d-%m-%Y"])
    location = CharField()
    beds = CharField()
    description = TextField()
    currency = CharField(null=True)
    price = CharField(null=True)

    class Meta:
        database = db


data = []
extra_tasks = []


async def get_page_data(session, page=None):
    if page:
        url = f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273"
    else:
        url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273"
    ua = UserAgent()
    headers = {
        "Accept": '*/*',
        "User-Agent": ua.random
    }

    async with session.get(url=url, headers=headers) as response:
        response_data = await response.text()

        soup = BeautifulSoup(response_data, "lxml")
        items_div = soup.find_all("div", class_="clearfix")
        if len(items_div) == 0:
            extra_tasks.append(page)
        for item in items_div[1:]:
            item_image = item.find("div", class_="image").find("img")

            try:
                image_src = item_image.get("data-src")
            except AttributeError:
                image_src = item_image.get("src")

            item_info = item.find("div", class_="info-container")
            title = item_info.find("div", class_="title").text.strip()

            price = item_info.find("div", class_="price").text.strip()

            location = item_info.find("div", class_="location").find("span").text.strip()
            item_date = item_info.find("div", class_="location").find("span", class_="date-posted").text
            try:
                date = datetime.strptime(item_date, '%d/%m/%Y').date().strftime('%d-%m-%Y')
            except ValueError:
                date = datetime.today().strftime('%d-%m-%Y')
            try:
                rental_info = item.find("div", class_="rental-info").find("span", class_="bedrooms").text.split()
            except AttributeError:
                rental_info =['None', "None"]
            description = item_info.find("div", class_="description").text.strip().split('...')[0] + "..."

            data_dict = {
                "image_src": image_src,
                "title": title,
                "date": date,
                "location": location,
                "beds": rental_info[1],
                "description": description
            }
            if bool(re.search(r'\d', price)):
                data_dict["currency"] = price[0]
                data_dict["price"] = price[1:]
            else:
                data_dict["currency"] = None
                data_dict["price"] = None
            data.append(data_dict)


async def get_page_count(extra_data=None):
    url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273"
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }
    async with aiohttp.ClientSession() as session:
        tasks = []
        if not extra_data:
            response = await session.get(url=url, headers=headers)
            soup = BeautifulSoup(await response.text(), "lxml")
            result_count = int(soup.find("div", class_="layout-3 new-real-estate-srp").find("div", class_="fes-pagelet").find("span").text.split()[5])
            task = asyncio.create_task(get_page_data(session))
            tasks.append(task)
            page_count = ceil(result_count / 45)
            page_range = range(2, page_count + 1)
        else:
            page_range = extra_data

        for page in page_range:
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    db.connect()
    db.create_tables([Info])
    asyncio.run(get_page_count())
    if extra_tasks:
        asyncio.run(get_page_count(extra_tasks))
    with db.atomic():
        for index in range(0, len(data), 50):
            Info.insert_many(data[index:index + 50]).execute()
    if not db.is_closed():
        db.close()


if __name__ == '__main__':
    main()
