import re
import time
import requests
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

def get_page(key_args):
	
	params = {
		"aid":"24",
		"app_name":"web_search",
		"offset":key_args.get("page"),
		"format":"json",
		"keyword":key_args.get("keyword"),
		"autoload":"true",
		"count":"20",
		"en_qc":"1",
		"cur_tab":"1",
		"from":"search_tab",
		"pd":"synthesis",
		"timestamp":str(int(round(time.time()*1000))),

	}

	headers = {
		"accept": "application/json, text/javascript",
		"accept-encoding": "gzip, deflate, br",
		"accept-language": "zh-CN,zh;q=0.9",
		"content-type": "application/x-www-form-urlencoded",
		"referer": "https://www.toutiao.com/search/?"+urlencode({"keyword":key_args.get("keyword")}),
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
		"x-requested-with": "XMLHttpRequest",
		"cookie":"csrftoken=fe7c26a51c9a0f2486c5de1431c1824f; tt_webid=6673058755394160136; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6673058755394160136; _ga=GA1.2.1406610621.1554379381; CNZZDATA1259612802=479162514-1541834355-%7C1568590246; s_v_web_id=19f22d86c87cae290348f1bcf67fdbb5; __tasessionId=4pceh62t11573970503028",
	}
	url = "https://www.toutiao.com/api/search/content/?"+urlencode(params)
	
	proxies = requests.get(url="http://49.235.221.86:5010/get/")
	my_proxy = {
		"http":"http://"+str(proxies.json().get("proxy")),
		#"https":"https://"+str(proxies.json().get("proxy"))

	}
	response = requests.get(url=url,headers=headers,proxies=my_proxy)
	try:

		if response.status_code == 200:
			html = response.json()
			if html.get("data") is not None:
				urls = []
				for item in html.get("data"):
					if item.get("title") is not None and item.get("article_url") is not None:
						urls.append(item.get('article_url'))
				return urls
	except RequestException:
		print("请求索引页出错")
		return None

def mutithreading(func,max_workers,args):

	event = []
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		for urls in executor.map(func,args):
			for data in executor.map(get_down,urls):
				break
		
def get_down(url):
	print(url)
	headers = {
		"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
		"accept-encoding": "gzip, deflate, br",
		"accept-language": "zh-CN,zh;q=0.9",
		"cache-control": "max-age=0",
		"cookie": "csrftoken=fe7c26a51c9a0f2486c5de1431c1824f; tt_webid=6673058755394160136; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6673058755394160136; _ga=GA1.2.1406610621.1554379381; CNZZDATA1259612802=479162514-1541834355-%7C1568590246; s_v_web_id=19f22d86c87cae290348f1bcf67fdbb5; ccid=afb2a720c31c1e62ddba9892c095b228; sso_auth_status=074b4c23aa90b6b0931c3182e3429d69; sso_uid_tt=9c505cdf04b23502b18072e3f1e563e7; toutiao_sso_user=eb69ecf3ff5e6894ade827ddd1a42707; passport_auth_status=dfa13a2f0c39bc82bfda90caf90645f1%2Cbd3424c5fe7f408d98dd5745f2cf63de%2C; sid_guard=c529d32e0699dcc8ebdda092f086a343%7C1573973805%7C5184000%7CThu%2C+16-Jan-2020+06%3A56%3A45+GMT; sid_tt=c529d32e0699dcc8ebdda092f086a343; sessionid=c529d32e0699dcc8ebdda092f086a343; uid_tt=9bf55981a51c21332cdcd063f13c01e932b04856fa07fd4c72e59a0d24bfca1a; __tea_sdk__ssid=undefined; __tasessionId=roz22lcye1573984493752",
		#"referer": "https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D",
		"sec-fetch-mode": "navigate",
		"sec-fetch-site": "same-origin",
		"sec-fetch-user": "?1",
		"upgrade-insecure-requests": "1",
		"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
	}

	response = requests.get(url,headers=headers)
	if response.status_code == 200:
		#print(response.text)
		pattern = re.compile('<meta charset=utf-8><title>(.*?)</title>',re.S)
		results =re.search(pattern,response.text)
		print(results) 
def main(pages,keyword):
	
	args = [{"page":page,"keyword":keyword} for page in range(pages+1)]
	html = mutithreading(get_page,1,args)
	
	

if __name__ == '__main__':
	
	url_lists = main(pages=1,keyword="街拍")

	



