from bs4 import BeautifulSoup
import requests
from src import get_proxy
from time import sleep


class CheckValid:
	headers = {
		'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; rev1.5; Windows NT 5.1; .NET CLR 1.1.4322)'
	}

	block_head = 'Размещен документ Протокол признания участника уклонившимся от заключения контракта от'

	def __init__(self, url: str, sids: list):
		self.url = url
		self.pages = sids

	def get_valid(self, num):
		tmp = None, None, None
		r = ''
		k = 0
		while True:
			try:
				proxy = get_proxy()
				URL = self.url.format(num)
				r = requests.get(URL, headers=self.headers, proxies={'http': proxy})
			except:
				k += 1
				continue
			r.encoding = r.apparent_encoding
			if r.status_code != 200:
				print(f'Статус запроса {r.status_code}')
				return tmp
			else:
				break
		bs = BeautifulSoup(r.text, 'html.parser')
		trs = bs.find_all('tr', attrs={'class': 'tableBlock__row'})
		print(f'Заявка №{num} Кол-во перезашрузок {k}')
		for i in trs:
			li = i.find('li')
			if self.block_head in str(li):
				auk = i.find('a').get('href').split('=')[1]
				tmp = (num, auk,)
				return tmp
			else:
				continue

	def start(self):
		li = []
		for i in self.pages:
			ans = self.get_valid(i)
			if not ans:
				print(f'Заявка №{i}\tне подходит')
			else:
				li.append(ans)
				print(f'Заявка №{i}\tинформация собрана')
			sleep(10)
		return li
