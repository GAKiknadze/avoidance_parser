from src import *
from src.base import DB
from src.main_page import MainPage
from src.check_valid import CheckValid
from src.valid_parser import ValidInfo
import asyncio
from time import sleep
from threading import Thread


BASE_NAME = 'base.sqlite3'
DRIVER_PATH = 'src/driver/chromedriver.exe'
START_URL = ''
SUPPLIRE_URL = ''
PAGE_SIZE = 0
STACK_SIZE = 0
DATES = '', ''


async def get_config():
	global START_URL
	global SUPPLIRE_URL
	global COMMON_URL
	global PAGE_SIZE
	global STACK_SIZE
	db = await DB.create(BASE_NAME)
	strt = await db.get_param('START_URL')
	supp = await db.get_param('SUPPLIRE_URL')
	comm = await db.get_param('COMMON_URL')
	page = await db.get_param('PAGE_SIZE')
	stack = await db.get_param('STACK_SIZE')
	START_URL = strt[0]
	SUPPLIRE_URL = supp[0]
	COMMON_URL = comm[0]
	PAGE_SIZE = int(page[0])
	STACK_SIZE = int(stack[0])


async def start_main_page():
	db = await DB.create(BASE_NAME)
	DATES = get_dates()
	print('Парсер ссылок запущен')
	m = MainPage(PAGE_SIZE, START_URL, DRIVER_PATH, DATES[1], DATES[1])
	items = m.run()
	await db.set_all_items(items)


def main_page():
	asyncio.run(start_main_page())


async def start_check_valid():
	db = await DB.create(BASE_NAME)
	print('Парсер валидных ссылок запущен')
	while True:
		ans = await db.get_all_items()
		ans = [i[0] for i in ans]
		cv = CheckValid(SUPPLIRE_URL, ans)
		v_items = cv.start()
		await db.set_valid_items(v_items)


def check_valid():
	asyncio.run(start_check_valid())


async def start_valid_info():
	db = await DB.create(BASE_NAME)
	v = ValidInfo(COMMON_URL, DRIVER_PATH)
	print('Парсер контрактов запущен')
	while True:
		ans = await db.get_valid_items()
		ans = v.start(ans)
		await db.set_data(ans)


def valid_info():
	asyncio.run(start_valid_info())


def run():
	for i in range(0, 5):
		thr = Thread(target=valid_info, args=())
		thr.start()
		sleep(3)

	for i in range(0, 5):
		thr = Thread(target=check_valid, args=())
		thr.start()
		sleep(3)

	while True:
		thr = Thread(target=main_page, args=())
		thr.start()
		sleep(240)


if __name__ == '__main__':
	asyncio.run(get_config())
	run()
