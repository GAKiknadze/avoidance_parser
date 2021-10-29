from selenium.webdriver import Chrome, ChromeOptions
from math import ceil
from time import sleep


class MainPage:
	userAgent = 'Mozilla/5.0 (X11; U; Linux; de-DE) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.8.0'
	
	def __init__(
			self, size: int,
			url: str, path: str,
			d_start: str, d_end: str
		):
		options = ChromeOptions()
		options.add_argument('--headless')
		options.add_argument(f'user-agent={self.userAgent}')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.driver = Chrome(executable_path=path, options=options)
		self.size = size
		self.url = url
		self.d_start = d_start
		self.d_end = d_end

	def get_length(self):
		URL = self.url.format(1, 10, self.d_start, self.d_end)
		self.driver.get(URL)
		total = self.driver.find_element_by_class_name('search-results__total')
		num = ''
		for i in total.text:
			if i.isdigit():
				num += i
		return int(num)

	def open(self, num: int=1):
		tmp = []
		URL = self.url.format(num, self.size, self.d_start, self.d_end)
		self.driver.get(URL)
		line = '//div[contains(text(), "Определение поставщика завершено")]'
		divs = self.driver.find_elements_by_xpath(line)
		for i in divs:
			item = ''
			par = i.find_elements_by_xpath('..')[0]
			head = par.find_element_by_class_name('registry-entry__header-mid__number')
			for j in head.text:
				if j.isdigit():
					item += j
			tmp.append((item,))
		return tmp

	def run(self):
		tmp = []
		li = self.get_length()
		pages = ceil(li / self.size)
		print(f'Кол-во страниц по запросу - {pages}')
		for i in range(1, pages + 1):
			try:
				ans = self.open(i)
			except:
				ans = []
			print(f'Страница поиска №{i}\tКол-во ОПЗ: {len(ans)}')
			tmp.extend(ans)
			sleep(5)
		return tmp

	def __del__(self):
		self.driver.close()

	def __exit__(self):
		self.__del__()
