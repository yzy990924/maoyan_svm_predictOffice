import requests
import font
from lxml import etree
import re, requests, time
import random

proxy_list = [
    '183.95.80.102:8080',
    '123.160.31.71:8080',
    '115.231.128.79:8080',
    '43.240.138.31:8080',
    '218.201.98.196:3128',
    '52.187.162.198:3128'
]
proxy = ['27.206.176.230:9000', '27.206.182.201:9000', '27.206.74.28:9000', '110.243.21.184:9999', '94.191.40.157:8118', '49.81.125.47:9000', '123.168.67.96:8118', '182.138.160.189:8118', '59.38.62.189:9797', '223.215.106.187:4216', '117.131.235.198:8060', '121.237.149.132:3000', '117.69.153.238:4216', '218.66.253.146:8486218.66.253.146:8486218.66.253.146:8800', '113.68.27.202:808', '182.148.15.88:8118', '36.112.139.146:3128', '60.191.11.237:3128', '49.85.211.224:8118']

# 构建头部，获取页面内容
def detail(url):
	
	header = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,application/signed-exchange;v=b3',
	'accept-encoding': 'gzip',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Cache-Control': 'max-age=0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
	}

	proxies = {'http':random.choice(proxy)}
	print(proxies)
	resp = requests.get(url, headers = header,proxies = proxies)
	resp = resp.text

	# 获取编码字典，并替换页面中的编码
	font_dict = font.getFont(resp)
	for key in font_dict.keys():
		resp = resp.replace(str(key), str(font_dict[key]))

	# 下面是额外内容：
	body = etree.HTML(resp)

	#获取电影名称
	name_info = body.xpath('//h1[@class="name"]/text()')[0]	

	#获取电影类型
	type_info = body.xpath('//li[@class="ellipsis"]')[0]	
	type_info = str(type_info.xpath('string(.)')).strip("\n").replace("\n",',').replace(' ','')
	
	#获取演职人员
	star = []
	director_star = body.xpath('//a[@class= "name"]/text()')
	for i in range(3):
		if(len(director_star)>i):
			star.append(director_star[i].replace("\n",',').replace(",",' ').replace(' ',' ')) 
		else:
			star.append(' ')

	#获取电影时长
	online_time = body.xpath('//li[@class="ellipsis"]')[2]	
	online_time = str(online_time.xpath('string(.)')).strip("\n")
	if(len(online_time)>10):
		online_time = online_time[:7]
	else :
		online_time = online_time[:4]
	
	#获取首周票房
	first =''
	if(body.xpath('//div[@class="film-mbox-item"]')!=[]):
		first_office = body.xpath('//div[@class="film-mbox-item"]')
		if(len(first_office)==3):	#可能存在有排名的情况
			first_office = first_office[1]
		else:
			first_office = first_office[0]
		first_office = str(first_office.xpath('string(.)')).replace(' ', '')
		first = first_office.split('\n')[1]

	#获取上映时间及地点
	time_info = body.xpath('//li[@class="ellipsis"]')[1]
	place_time = str(time_info.xpath('string(.)')).strip("\n")
	if(len(place_time.split('/'))!=1):
		place = place_time.split('/')[0].strip()
		time = place_time.split('/')[1].strip()
	else :
		time = ''
		place = place_time.replace(' ',' ')

	#获取评分及评分人数
	mark_info = body.xpath('//div[@class="movie-index"]/div')
	mark = mark_info[0].xpath('string(.)').replace(' ', '')
	mark = re.sub(r'\n+', '|', mark)[1:-1].split('|')
	if len(mark) < 2:
		myMark = ''
		myNum = ''
	else:
		myMark = mark[0]
		myNum = mark[1][:-3]

	#将累计票房中的亿/万替换为数字	
	boxOffice = mark_info[1].xpath('string(.)').replace(' ', '').replace('\n', '')
	if(boxOffice!='暂无'):
		wanyuan = re.sub("[A-Za-z0-9\\!\\%\\[\\]\\,\\。\\.]", "", boxOffice)
		totalCount = float(re.findall(r'-?\d+\.?\d*e?-?\d*?', boxOffice)[0])#方便计算, 转换为数字
		if(wanyuan=='亿'):
			totalCount = totalCount*100000000
		else :
			if(wanyuan=='万'):
				totalCount = totalCount*10000
		boxOffice = int(totalCount)

	movie = [name_info,place,online_time,type_info,time,myMark,myNum,first,boxOffice,star[0],star[1],star[2]]
	#['名称','上映地区','上映时间','类型','时长','评分','评分人数','首周票房','累计票房','演职人员1','演职人员2','演职人员3']
	return (movie)	#返回此电影的相关数据
