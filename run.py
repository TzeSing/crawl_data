# -*- coding: utf-8 -*-
"""requests爬取所有链接，然后再分批爬取链接里的内容
"""
import json
import random
import time

import requests
from lxml import etree
from environs import Env
import pymysql
from pymysql.converters import escape_string


env = Env()
env.read_env()

host = env.str("host")
user = env.str("user")
pwd = env.str("pwd")
db = env.str("db")
conn = pymysql.connect(host=host, user=user, passwd=pwd, database=db)

c = conn.cursor()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'lianjia_uuid=c8661046-07e4-4186-aab3-55784a700f83; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217913c5993788-020541bbd4c4b-d7e163f-1327104-17913c59938811%22%2C%22%24device_id%22%3A%2217913c5993788-020541bbd4c4b-d7e163f-1327104-17913c59938811%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyguangzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=440100; lianjia_ssid=293d7a69-8cd2-4ba9-9510-b2351a18b1e7; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1619534387,1619709271,1619840565; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1619840963; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYjU2YjBmOWQ3YmFhYmIxNzExNTUzNDEyMDZjNjI1NTEwYTRkNWY2OTZhZDdiNWY5Njg4OTFiOGM0N2FlZTE1NGMyZmRmZjUyMDEzYjFkNGFmODY1YzY0ZDk0ZDEzZDNiYTEyMGFiNGU3Yzg0ZmQ2ZjkzMjIwNjY3ZDY4MmE0ZjRkOWQ4YmU0NTM5NjZkM2IxZjI3N2NmYWIxZTFkYTQ2MmEzNzg4NGY1ZDkzNDBjY2VjN2EyNjYyNzRkNzFlN2M0ZjY1ZTk1MzRmOGJlMWU1N2U5YzZjYTM0MjhmYWI3MzdlYmNhOGEyYzM1MGMxOWQ3YjY0M2U5YmM4NDdmNDk4MzVmNjQ2MjAxY2ZhM2ZmZDliNTI0Zjg3NTM3NjA5YTZiYmJkMWE2MzY5OGRiOGMyN2Y1ZmQ0ZTI2MWU2MGUzZWNcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiYjQ3YTI0NWVcIn0iLCJyIjoiaHR0cHM6Ly9nei5rZS5jb20vZXJzaG91ZmFuZy90aWFuaGUvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=',
    'Host': 'gz.ke.com',
    'Pragma': 'no-cache',
    'Referer': 'https://gz.ke.com/ershoufang',
    'Content-Type': 'text/plain;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

with open('house_url_distinct.txt', 'r', encoding='utf-8') as f:
    urls = f.read().strip().split('\n')

# urls = ['https://gz.ke.com/ershoufang/108402144930.html?fb_expo_id=440842182929846274']
for i, url in enumerate(urls):
    time.sleep(2 + round(random.random(), 2))
    if i % 1000 == 0:
        print('已完成1000个')
    resp = requests.get(url, headers=headers)
    # if resp.status_code != 200:
    url = url.split('?')[0]

    tree = etree.HTML(resp.content)

    # 标题和关注数
    title_elem = tree.xpath(
        '//div[@data-component="detailHeader"]/div[@class="detailHeader VIEWDATA"]')
    title = etree.tostring(title_elem[0], method='html', encoding='utf-8').decode('utf-8')

    # 价格区域等
    overview_intro_elem = tree.xpath('//div[@data-component="overviewIntro"]//div[@class="content"]')
    overview_intro = etree.tostring(overview_intro_elem[0], method='html', encoding='utf-8').decode('utf-8')

    # 基本信息
    m_content_elem = tree.xpath('//div[@class="m-content"]/div[@class="box-l"]')
    m_content = etree.tostring(m_content_elem[0], method='html', encoding='utf-8').decode('utf-8')

    try:
        c.execute("""INSERT INTO log(url, title, overview_intro, m_content) VALUES(%s, %s, %s, %s)"""
                  ,(url, title, overview_intro, m_content))
        conn.commit()
    except:
        print(url + ' insert wrong!!!')
        conn.rollback()

conn.close()
