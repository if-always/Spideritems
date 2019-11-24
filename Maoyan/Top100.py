import re
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

class ManyanSpider(object):
	"""docstring for ManyanSpider"""
	def __init__(self):
		
		self.headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "zh-CN,zh;q=0.9",
		"Cache-Control": "max-age=0",
		"Connection": "keep-alive",
		"Cookie": "__mta=150822153.1573879290040.1574572229905.1574572624184.16; uuid_n_v=v1; uuid=59175A20082B11EA80DEBB1F518E903DABD6A577B18C41F89FBA9F8A0D5585F7; _lxsdk_cuid=16e72841832c8-08dbb5e86265c7-5b123211-100200-16e72841833c8; _lxsdk=59175A20082B11EA80DEBB1F518E903DABD6A577B18C41F89FBA9F8A0D5585F7; _csrf=6ba3659b3536fb515560892e099eb8714b08bbbc6f43b175dbc49d83519eccea; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1573879290,1574569044; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=150822153.1573879290040.1574569103486.1574569108581.12; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1574572624; _lxsdk_s=16e9bfd3512-f0b-07b-ab8%7C%7C1",
		"Host": "maoyan.com",
		"Referer": "https://maoyan.com/board/4?offset=0",
		"Sec-Fetch-Mode": "navigate",
		"Sec-Fetch-Site": "same-origin",
		"Sec-Fetch-User": "?1",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
		}

		self.session = requests.session()

	def __get_resp(self,url):

		response = self.session.get(url=url,headers=self.headers)
		if response.status_code ==200:
			return response
		return None

	def __get_parse_page(self,url):

		html = self.__get_resp(url).text
		pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)@.*?"name"><a.*?">(.*?)</a>.*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?"integer">(.*?)</i><i class="fraction">(.*?)</i></p>',re.S)
		items = re.findall(pattern,html)
		for item in items:
			yield{
				"index":item[0],
				"image":item[1],
				"title":item[2],
				"actor":item[3].strip(),
				"times":item[4].strip()[5:],
				"score":item[5]+item[6]

			}


	def mutithreading(self,args):
		with ThreadPoolExecutor(max_workers=2) as executor:
			for datas in executor.map(self.__get_parse_page,args):
				for data in datas:
					print(data)

	def run(self):

		self.originurl = "https://maoyan.com/board/4?offset="
		self.url_lists = [self.originurl+str(10*i) for i in range(0,10)]
		self.mutithreading(self.url_lists)

if __name__ == '__main__':
	s = ManyanSpider()
	s.run()