from bs4 import BeautifulSoup
import requests
import json
from requests.exceptions import RequestException
import time
import pandas as pd
import requests
import re
import os
from fontTools.ttLib import TTFont
import movie_detail
import xlwt
import random
proxy_list = [
    '183.95.80.102:8080',
    '123.160.31.71:8080',
    '115.231.128.79:8080',
    '166.111.77.32:80',
    '43.240.138.31:8080',
    '218.201.98.196:3128'
]

proxy = ['27.206.176.230:9000', '27.206.182.201:9000', '27.206.74.28:9000', '110.243.21.184:9999', '94.191.40.157:8118', '49.81.125.47:9000', '123.168.67.96:8118', '182.138.160.189:8118', '59.38.62.189:9797', '223.215.106.187:4216', '117.131.235.198:8060', '121.237.149.132:3000', '117.69.153.238:4216', '218.66.253.146:8486218.66.253.146:8486218.66.253.146:8800', '113.68.27.202:808', '182.148.15.88:8118', '36.112.139.146:3128', '60.191.11.237:3128', '49.85.211.224:8118']

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}
global test_data 
test_data = [['名称','上映地区','上映时间','类型','时长','评分','评分人数','首周票房','累计票房','演职人员1','演职人员2','演职人员3']]

# 获取网页
def GetHtml(url):
    try:
        proxies = {'http':random.choice(proxy)}
        print(proxies)
        # 修改网页的头部
        r = requests.get(url,headers = header,proxies = proxies)
        # 查看网页是否访问成功
        r.raise_for_status()
        # 将网页解析内容转换为 utf-8 形式
        r.encoding = r.apparent_encoding
        # print(r.read().decode("utf-8"))
        print(r.url)
        return r.text
    except RequestException:
        return '访问失败'

# 获取该网页的电影信息
def parse_one_page(html):
    # 将网页 html 代码转换为BeautifulSoup 能读懂的形式
    soup = BeautifulSoup(html, 'lxml')
    # 查找该页所有的电影, 返回列表形式，列表里是每个电影的信息
    info = soup.find_all('dd')
    office = 10
    global test_data
    for i in info:
        #获取电影的id
        id = i.a['href']
        print(id)
        url = 'https://maoyan.com'+id
        data = movie_detail.detail(url)#调用电影详情页函数
        test_data.append(data)#将这条电影数据加入总数据中
    return test_data

# 储存为 xls 格式     
def write_to_xls(xls_data):
    # 创建工作簿
    f = xlwt.Workbook()
    # 创建一个sheet
    sheet1 = f.add_sheet('test', cell_overwrite_ok = True)
    for i in range(len(test_data)):
        t = test_data[i]
        for j in range(len(t)):
            sheet1.write(i, j, t[j])
    # 保存文件
    # f.save("d:\\high_score.xls")
    f.save("d:\\2018.xls")
       
def main(offset):
    # 获取网页网址
    url = 'https://maoyan.com/films?yearId=13&showType=3&sortId=1&offset=' + str(offset)#2019年
    html = GetHtml(url)
    content = parse_one_page(html)

if __name__ == "__main__":
     # 获取每一页电影的信息  
    for i in range(5,6):
        main(offset = i * 30)
        time.sleep(1)
    write_to_xls(test_data)



 
