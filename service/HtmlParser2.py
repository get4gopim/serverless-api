# HTML Web Scrabbing Forecast helper file


import logging
import os
import asyncio
import sys
import threading
from queue import Queue

import async_timeout
import time
import aiohttp
import schedule

from model import FuelInfo, RateInfo, WeatherInfo, WeatherForecast
from utility import util

from bs4 import BeautifulSoup
from aiohttp import ClientSession, ClientConnectorError, TCPConnector

weather_url = 'https://weather.com/en-IN/weather/today/l/'
gold_url = 'http://www.livechennai.com/gold_silverrate.asp'
fuel_url = 'https://www.livechennai.com/petrol_price.asp'

google_weather_url = 'https://www.google.com/search?q=weather'
default_location = 'chennai'
DEFAULT_LOC_UUID = '4ef51d4289943c7792cbe77dee741bff9216f591eed796d7a5d598c38828957d'

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
LOGGER = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT}


async def fetch(session, url):
    try:
        async with async_timeout.timeout(30):
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise Exception(f'Response Status {response.status} is not OK')
    except asyncio.TimeoutError as ex:
        LOGGER.error(f'Unable to connect remote API : {url} - {repr(ex)}')
        raise ex


async def get_weather(future, location):
    start = time.time()

    if location is not None:
        url = weather_url + location
    else:
        url = weather_url + DEFAULT_LOC_UUID

    info = None
    LOGGER.info(url)

    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            html = await fetch(session, url)
            LOGGER.info(f'weather content fetch in {time.time() - start} secs.')
            parse_start = time.time()
            info = await parse_weather(html)
            LOGGER.info(f'weather parsing took {time.time() - parse_start} secs.')
    except ClientConnectorError as ex:
        LOGGER.error(f'Unable to connect Weather API : {repr(ex)}')
        LOGGER.error(ex)
        info = WeatherInfo.WeatherInfo('0', "0", "0", "00:00", "", "", "")
        info.set_error(ex)
    except BaseException as ex:
        LOGGER.error(f'Unable to connect Weather API :- {repr(ex)}')
        LOGGER.error(ex)
        info = WeatherInfo.WeatherInfo('0', "0", "0", "00:00", "", "", "")
        info.set_error(ex)

    LOGGER.info (f'Weather Time Taken {time.time() - start}')
    future.set_result(info)


async def get_weather_forecast(future, location):
    start = time.time()

    if location is not None:
        url = weather_url + location
    else:
        url = weather_url + DEFAULT_LOC_UUID

    info = None
    LOGGER.info(url)

    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            html = await fetch(session, url)
            LOGGER.info(f'weather content fetch in {time.time() - start} secs.')
            parse_start = time.time()
            info = await parse_weather_forecast(html)
            LOGGER.info(f'weather parsing took {time.time() - parse_start} secs.')
    except ClientConnectorError as ex:
        LOGGER.error(f'Unable to connect Weather API : {repr(ex)}')
        info = []
    except BaseException as ex:
        LOGGER.error(f'Unable to connect Weather API : {repr(ex)}')
        info = []

    LOGGER.info (f'Weather Time Taken {time.time() - start}')
    future.set_result(info)


async def get_google_forecast(future, location):
    start = time.time()

    if location is not None:
        url = google_weather_url + '+' + location
    else:
        url = google_weather_url + '+' + default_location

    info = None
    LOGGER.info(url)

    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            html = await fetch(session, url)
            LOGGER.info(f'weather content fetch in {time.time() - start} secs.')
            parse_start = time.time()
            info = await parse_google_forecast(html)
            LOGGER.info(f'weather parsing took {time.time() - parse_start} secs.')
    except ClientConnectorError as ex:
        LOGGER.error(f'Unable to connect Weather API : {repr(ex)}')
        info = []
    except BaseException as ex:
        LOGGER.error(f'Unable to connect Weather API : {repr(ex)}')
        info = []

    LOGGER.info (f'Weather Time Taken {time.time() - start}')
    future.set_result(info)


async def get_gold_price(future):
    start = time.time()
    info = None
    try:
        async with ClientSession() as session:
            html = await fetch(session, gold_url)
            LOGGER.info(f'gold content fetch in {time.time() - start} secs.')
            parse_start = time.time()
            info = await parse_gold_info(html)
            LOGGER.info(f'gold parsing took {time.time() - parse_start} secs.')
    except ClientConnectorError as ex:
        LOGGER.error(f'Unable to connect Gold API : {repr(ex)}')
        info = RateInfo.RateInfo('0', '0', '0.0', "", "")
        info.set_error(ex)
    except BaseException as ex:
        LOGGER.error(f'Unable to connect Gold API : {repr(ex)}')
        info = RateInfo.RateInfo('0', '0', '0.0', "", "")
        info.set_error(ex)

    LOGGER.info(f'Gold Time Taken {time.time() - start}')
    future.set_result(info)


async def get_fuel_price(future):
    start = time.time()
    info = None

    try:
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, fuel_url)
            LOGGER.info(f'fuel content fetch in {time.time() - start} secs.')
            parse_start = time.time()
            info = await parse_fuel_info(html)
            LOGGER.info(f'fuel parsing took {time.time() - parse_start} secs.')
    except ClientConnectorError as ex:
        LOGGER.error(f'Unable to connect Fuel API : {repr(ex)}')
        info = FuelInfo.FuelInfo('0', '0', "", "")
        info.set_error(ex)
    except BaseException as ex:
        LOGGER.error(f'Unable to connect Weather API : {repr(ex)}')
        info = FuelInfo.FuelInfo('0', '0', "", "")
        info.set_error(ex)

    LOGGER.info(f'Fuel Time Taken {time.time() - start}')
    future.set_result(info)


async def get_google_weather(future, location):
    start = time.time()
    info = None
    if location is not None:
        url = google_weather_url + '+' + location
    else:
        url = google_weather_url + '+' + default_location

    LOGGER.info (url)

    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            html = await fetch(session, url)
            LOGGER.info(f'g-weather content fetch in {time.time() - start} secs.')
            parse_start = time.time()
            info = await parse_google_weather(html)
            LOGGER.info(f'g-weather parsing took {time.time() - parse_start} secs.')
    except BaseException as ex:
        LOGGER.error(f'Unable to connect Weather API : {repr(ex)}')
        info = WeatherInfo.WeatherInfo('0', "0", "0", "00:00", "", "", "")
        info.set_error(ex)

    LOGGER.info (f'Weather Time Taken {time.time() - start}')
    future.set_result(info)


async def parse_google_weather(page_content):
    soup = BeautifulSoup(page_content, 'lxml')

    seg_temp = soup.find_all('div', {'id': 'wob_wc'})[0]
    # print(seg_temp.text)
    # seg_temp = soup.find_all('div#wob_wc')
    # seg_temp = soup.find('div', class_='vk_c card-section')
    # print (seg_temp)

    span = seg_temp.select('span')[0]       # First Segment
    element = span.select('div#wob_loc')[0]
    location = element.text

    as_of = ''
    # element = span.select('div#wob_dts')[0]
    # as_of = element.text

    element = span.select('span#wob_dc')[0]
    condition = element.text

    div_sub = seg_temp.select('div#wob_d')[0]   # Second Segment

    element = div_sub.select('span#wob_tm')[0]
    temp = element.text

    div_sub = seg_temp.find_all('div', class_='vk_gy vk_sh')[1] # Second Sub

    element = div_sub.select('span#wob_hm')[0]
    humidity = element.text

    element = div_sub.select('span#wob_pp')[0]
    precipitation = element.text
    idx = util.index_of(precipitation, '%')
    if idx > 0:
        precipitation = precipitation + ' chance of rain until'

    # fetch low and high temperature for the day
    high = low = temp
    # div_forecast = seg_temp.find('div', class_='wob_df wob_ds') # Third Segment
    # div_sub = div_forecast.find('div', class_='vk_gy')
    # span = div_sub.select('span')[0]
    # high = span.text
    #
    # div_sub = div_forecast.find_all('div')[4]
    # span = div_sub.select('span')[0]
    # low = span.text

    weatherInfo = WeatherInfo.WeatherInfo(temp, low, high, as_of, condition, location, precipitation)
    weatherInfo.set_humidity(humidity)
    weatherInfo.set_error(None)

    LOGGER.info(str(weatherInfo))

    return weatherInfo


async def parse_weather(page_content):
    soup = BeautifulSoup(page_content, 'lxml') # html.parser # lxml # html5lib

    seg_temp = soup.find_all('div', {'id' : 'WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034'})[0]
    # print(seg_temp.text)

    seg_temp = seg_temp.find_all('div', recursive=False)[0]
    seg_temp = seg_temp.find_all('section', recursive=False)[0]
    seg_temp = seg_temp.find_all('div', recursive=False)[0]
    div_ele = seg_temp.find_all('div', recursive=False)[0]
    # print(div_ele)

    location = div_ele.find('h1')
    location = location.text
    idx = util.index_of(location, ' Weather')
    if idx > 0:
        location = location[0:idx]

    as_of = div_ele.find('div')
    as_of = as_of.text
    idx = util.index_of(as_of, "as of ")
    idx_ist = util.index_of(as_of, " IST")
    if idx > 0:
        as_of = as_of[idx+6:idx_ist]

    div_ele = seg_temp.find_all('div', recursive=False)[1]
    # print(div_ele)
    div_cond = div_ele.find_all('div', recursive=False)[0]
    # print(div_cond)
    element = div_cond.find('span')
    temp = element.text
    if len(temp) == 3:
        temp = temp[0:2]

    element = div_cond.find('div')
    condition = element.text

    div_cond = div_ele.find_all('div', recursive=False)[1]
    div_cond = div_cond.find_all('div', recursive=False)[0]
    element = div_cond.find_all('span')[0]
    high = element.text
    element = div_cond.find_all('span')[1]
    low = element.text

    if high == '--':
        high = temp

    if len(high) == 3:
        high = high[0:2]

    if len(low) == 3:
        low = low[0:2]

    preciption = seg_temp.find_all('div', recursive=False)[2]
    # print(preciption)
    if preciption is not None:
        preciption = preciption.text
    else:
        preciption = ''

    seg_temp = soup.find_all('div', {'id': 'todayDetails'})
    # seg_temp = soup.find_all('div', {'id': 'WxuTodayDetails-main-fd88de85-7aa1-455f-832a-eacb037c140a'})
    if seg_temp is not None and len(seg_temp) > 0:
        seg_temp = seg_temp[0]
        # print(seg_temp)
        div_ele = seg_temp.find('section')
        div_ele = div_ele.find_all('div', recursive=False)[1]
        div_node = div_ele.find_all('div', recursive=False)[2]
        # div_ele = div_node.find_all('div', recursive=False)[0]
        # print(div_ele.text)
        div_ele = div_node.find_all('div', recursive=False)[1]
        # print(div_ele)
        humidity = div_ele.text
    else:
        humidity = '0'

    weatherInfo = WeatherInfo.WeatherInfo(temp, low, high, as_of, condition, location, preciption)
    weatherInfo.set_humidity(humidity)
    weatherInfo.set_error(None)
    LOGGER.info(str(weatherInfo))

    return weatherInfo


async def parse_google_forecast(page_content):
    soup = BeautifulSoup(page_content, 'lxml') # html.parser # lxml # html5lib

    seg_temp = soup.find_all('div', {'id': 'wob_wc'})[0]
    # seg_temp = soup.find_all('div#wob_wc')
    # seg_temp = soup.find('div', class_='vk_c card-section')
    # print (seg_temp)

    # div_section = seg_temp.find_all('div')

    div_section = seg_temp.find_all('div', recursive=False)[3]
    # print(div_section)

    div_section = div_section.find_all('div', recursive=False)[0]
    # print(div_section)
    div_section = div_section.find_all('div', recursive=False)

    list = []
    for element in div_section:
        sub_div = element.find_all('div', recursive=False)
        next_day = sub_div[0].text

        sub_ele = sub_div[1].find('img')
        condition = sub_ele.get('alt')
        # print(condition)

        sub_ele = sub_div[2].find_all('div')[0]
        sub_ele = sub_ele.find_all('span', recursive=False)
        next_day_low = sub_ele[0].text

        sub_ele = sub_div[2].find_all('div')[1]
        sub_ele = sub_ele.find_all('span', recursive=False)
        next_day_temp = sub_ele[0].text

        forecast = WeatherForecast.WeatherForecast(next_day, next_day_temp, next_day_low, condition,
                                                   'next_day_preciption.text')
        forecast.set_error(None)
        list.append(forecast)
        LOGGER.info(str(forecast))

    # print (len(list))

    return list


async def parse_weather_forecast(page_content):
    soup = BeautifulSoup(page_content, 'lxml') # html.parser # lxml # html5lib

    seg_temp = soup.find_all('div', {'id' : 'WxuDailyWeatherCard-main-bb1a17e7-dc20-421a-b1b8-c117308c6626'})[0]
    # print(seg_temp.text)

    seg_temp = seg_temp.find('section')
    location = seg_temp.find('div')
    location = seg_temp.find('ul')
    # print(location.text)

    day = location.find_all('li')
    print('\n')

    list = []
    for element in day:
        next_day = element.find('h3')
        # print(next_day)

        div_ele = element.find_all('div')

        next_day_temp = div_ele[0]
        next_day_temp = next_day_temp.text
        if len(next_day_temp) == 3:
            next_day_temp = next_day_temp[0:2]

        next_day_low = div_ele[1]
        next_day_low = next_day_low.text
        if len(next_day_low) == 3:
            next_day_low = next_day_low[0:2]

        condition = "Cloudy"
        next_day_condition = div_ele[2]
        # print(next_day_condition)

        next_day_preciption = div_ele[3]

        if next_day_condition is not None:
            next_day_condition = next_day_condition.find('svg')

            if next_day_condition is not None:
                next_day_condition = next_day_condition.find('mask')

                if next_day_condition is not None:
                    condition = next_day_condition.get('id')

        # print(next_day.text + ' ' + next_day_temp.text + ' ' + next_day_low.text + ' ' + next_day_preciption.text + ' ' + next_day_condition)

        forecast = WeatherForecast.WeatherForecast(next_day.text, next_day_temp , next_day_low, condition, next_day_preciption.text)
        forecast.set_error(None)
        list.append(forecast)
        LOGGER.info(str(forecast))

    # print (len(list))

    return list


async def parse_gold_info(page_content):
    soup = BeautifulSoup(page_content, 'lxml')

    table = soup.select('table.table-price').__getitem__(1)
    rows = table.find_all('tr')

    # print (last_updated)

    gold_date = str(rows[2].find_all('td')[0].text).strip()
    gold_24 = str(rows[2].find_all('td')[1].text).strip()
    gold_22 = str(rows[2].find_all('td')[3].text).strip()

    # print (gold_22 + " " + gold_24 + " " + gold_date)

    table = soup.select('table.table-price').__getitem__(3)
    rows = table.find_all("tr")

    silver_date = str(rows[1].find_all('td')[0].text).strip()
    silver = str(rows[1].find_all('td')[1].text).strip()

    # print (silver_date + " " + silver)

    last_updated = soup.find_all('p', class_='mob-cont')[0]
    last_updated = last_updated.text.strip()
    idx = util.index_of(last_updated, ":")
    if idx > 0:
        last_updated = last_updated[idx + 1:len(last_updated)]

    rate_info = RateInfo.RateInfo(gold_22, gold_24, silver, gold_date, last_updated)
    rate_info.set_error(None)
    LOGGER.info(str(rate_info))

    return rate_info


async def parse_fuel_info(page_content):
    soup = BeautifulSoup(page_content, 'lxml')

    table = soup.select("table#BC_GridView1").__getitem__(0)
    # print (table)

    rows = table.find_all("tr")
    fuel_date = rows[1].find_all('td')[0].text
    petrol_price = str(rows[1].find_all('td')[1].text).strip()

    table = soup.select("table#BC_GridView1").__getitem__(1)
    # print (table)

    rows = table.find_all("tr")
    fuel_date = rows[1].find_all('td')[0].text
    diesel_price = str(rows[1].find_all('td')[1].text).strip()

    table = soup.find_all('table', {'id': 'tableb'}).__getitem__(1)
    # print (table)
    rows = table.find_all("tr")
    # print(rows)
    last_updated = rows[0].find_all('td', {'id': 'subcell'})[0]
    last_updated = last_updated.find_all('div')[3]

    # print (last_updated.text)
    last_updated = last_updated.text
    idx = util.index_of(last_updated, 'from ')
    if idx > 0:
        last_updated = last_updated[idx + 5:len(last_updated)]

    fuel_info = FuelInfo.FuelInfo(petrol_price, diesel_price, fuel_date, last_updated)
    fuel_info.set_error(None)

    LOGGER.info(str(fuel_info))

    return fuel_info


# Testing Methods
def callback(future):
    print (future.result())


def test_async_future(location):
    start = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    f1 = asyncio.Future()
    f2 = asyncio.Future()
    f3 = asyncio.Future()

    f1.add_done_callback(callback)
    f2.add_done_callback(callback)
    f3.add_done_callback(callback)

    # tasks = [get_google_weather(f1), get_gold_price(f2), get_fuel_price(f3)]
    tasks = [get_gold_price(f2), get_fuel_price(f3)]
    if location is not None:
        tasks.append(get_google_weather(f1, location))
    else:
        tasks.append(get_weather(f1))

    loop.run_until_complete(asyncio.wait(tasks))

    loop.close()

    LOGGER.info(f'Total Time Taken {time.time() - start}')
    print ('\n\n')


def call_weather_api(location):
    LOGGER.info("call_weather_api")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    f1 = asyncio.Future()

    f1.add_done_callback(callback)

    tasks = []
    # tasks.append(get_google_forecast(f1, location))
    # tasks.append(get_google_weather(f1, location))
    # tasks.append(get_weather(f1, location))
    # tasks.append(get_weather_forecast(f1, location))

    if util.is_uuid(location):
        tasks.append(get_weather(f1, location))
    else:
        tasks.append(get_google_weather(f1, location))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    return f1.result()


def call_weather_forecast(location):
    LOGGER.info("call_weather_forecast")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    f1 = asyncio.Future()

    f1.add_done_callback(callback)

    tasks = []
    if util.is_uuid(location):
        tasks.append(get_weather_forecast(f1, location))
    else:
        tasks.append(get_google_forecast(f1, location))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    return f1.result()


def call_gold_api():
    LOGGER.info("call_gold_api")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    f1 = asyncio.Future()

    f1.add_done_callback(callback)

    tasks = [get_gold_price(f1)]
    loop.run_until_complete(asyncio.wait(tasks))

    loop.close()
    print()


def worker_main():
    while True:
        try:
            job_func, job_args = jobqueue.get()
            job_func(*job_args)
            jobqueue.task_done()
        except BaseException as e:
            print(e)
            LOGGER.error(f'worker_main : {repr(e)}')


jobqueue = Queue()

if __name__ == '__main__':
    LOGGER.info (f"Parser starts ... args: {len(sys.argv)}")

    call_weather_api('thalambur')
    # call_weather_api('4ef51d4289943c7792cbe77dee741bff9216f591eed796d7a5d598c38828957d')