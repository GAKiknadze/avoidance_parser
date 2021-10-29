from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from random import randint


def get_dates():
	td1 = timedelta(days=1)
	date = datetime.now()
	pre_date = date - td1
	md = date.date().month
	mt = pre_date.date().month
	md = '0' + str(md) if md < 10 else md
	mt = '0' + str(mt) if mt < 10 else mt
	now = '{}.{}.{}'.format(date.date().day, md, date.date().year)
	pre = '{}.{}.{}'.format(pre_date.date().day, mt, pre_date.date().year)
	return pre, now


def get_length(dates):
	url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&updateDateFrom={}&updateDateTo={}&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes=&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'
	url = url.format(dates[0], dates[1])
	headers = {
		'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1)'
	}
	r = requests.get(url, headers=headers)
	bs = BeautifulSoup(r.text, 'html.parser')
	total = bs.find('div', attrs={'class': 'search-results__total'}).text
	line = [i for i in total if i.isdigit()]
	return int(''.join(line))


def random_proxy():
	PROX_NAME = './proxies'
	f = open(PROX_NAME)
	proxies = f.read().split('\n')
	f.close()
	ind = randint(0, len(proxies) - 1)
	proxy = proxies[ind]
	return proxy


def get_proxy():
	url = 'https://zakupki.gov.ru'
	headers = {
		'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1)'
	}
	while True:
		proxy = random_proxy()
		try:
			r = requests.get(url, headers=headers, proxies={'http': proxy})
		except:
			continue
		if r.status_code == 200:
			return proxy