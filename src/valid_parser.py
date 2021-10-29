from selenium.webdriver import Chrome, ChromeOptions
from time import sleep


class ValidInfo:
	headers = {
		'user-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061003 BonEcho/2.0'
	}

	def __init__(self, url: str, path: str):
		self.url = url
		options = ChromeOptions()
		options.add_argument('--headless')
		options.add_argument(f'user-agent={self.headers["user-agent"]}')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.driver = Chrome(executable_path=path, options=options)

	def get_valid(self, num):
		URL = self.url.format(num)
		self.driver.get(URL)
		cont = self.driver.find_elements_by_xpath('//div[@class="row blockInfo"]')[-1]
		infs = cont.find_elements_by_xpath('//span[@class="section__info"]')
		name = infs[-3].text
		inn = infs[-2].text
		if inn == 'Да':
			inn = infs[-1].text
			if inn == 'Да':
				inn = 'Не найден'
		return (num, name, inn, None, None, 1)

	def start(self, pages: list):
		li = []
		for i in pages:
			ans = self.get_valid(i[1])
			if not ans:
				print(f'Контракт №{i[1]}\tне подходит')
			else:
				li.append((None, i[0], *ans))
				print(f'Контракт №{i[1]}\tинформация собрана')
			sleep(10)
		return li

	def __del__(self):
		self.driver.close()

	def __exit__(self):
		self.__del__()
