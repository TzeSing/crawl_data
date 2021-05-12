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

s = requests.session()
s.keep_alive = False

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
    'Connection': 'close',  # 不要keep-alive
    # 'Cookie': 'lianjia_uuid=134c13b6-6255-4895-9f81-7c6df0dce4ce; _smt_uid=60867371.535bd856; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1619420240,1619423337,1619501815; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221790cf76bee71b-00b8a87eec5642-3f356b-2073600-1790cf76befcc7%22%2C%22%24device_id%22%3A%221790cf76bee71b-00b8a87eec5642-3f356b-2073600-1790cf76befcc7%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyguangzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=440100; lianjia_ssid=77306332-426d-4982-ad35-4660368273bb; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1620293661; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYzE2OTlhMTMxZTA3OGFhNTJjMGJlNWM4OTE0NDc5ZWNkNjI0NTAwNjMyY2FlZWI0NjA0NDk3ODFkZWI5MTAxZDMwODU4OWRkYjEwNjQ0ZGYyYjVlMDkzYWE2NGY3MTVmZDhlZGY1ZGZlY2M3Njk5YWE4NzY2NjA5MDZlYjAwMmZhMWE5ZWJkODAwYTMwYTdkNjVkMGU3YzZkMjdmZDAzODBhNjMyNTk2OGY4YWY1ZmUxZTQ1MWExMWU4MGFmNGYzZmYzZjJhNDNmMTA4N2U0MTdmMDMzYWFkZTJiN2U2MDhhYmIwYjJjNTU1Njg3NWQxY2RjNzVkZjQ4MjkxZWJjNzg5MjgwYjBhNDIyYWZkYzY3MmJkMDM5MjYzZTkxYzZlOTU3MmFmZTU2ZDQ2NTRmZWNlMWMyMjc0OTEyYzczZTNmNDQ2M2FlYTg1NzBjY2M5YTBlNDNmNWNlMmE4ODg0NlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjMjg4YjRlNVwifSIsInIiOiJodHRwczovL2d6LmtlLmNvbS9lcnNob3VmYW5nLzEwODQwMjE0NDkzMC5odG1sP2ZiX2V4cG9faWQ9NDQwODQyMTgyOTI5ODQ2Mjc0Iiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=',
    'Host': 'gz.ke.com',
    'Pragma': 'no-cache',
    'Referer': 'https://gz.ke.com/ershoufang',
    'Content-Type': 'text/plain;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

with open('house_url_distinct.txt', 'r', encoding='utf-8') as f:
    urls = f.read().strip().split('\n')

c.execute('SELECT url FROM log')
crawled_urls = c.fetchall()
crawled_urls = set([i[0] for i in crawled_urls])

# urls = ['https://gz.ke.com/ershoufang/108402144930.html?fb_expo_id=440842182929846274']
skip_status = False
for i, url in enumerate(urls):
    if not skip_status:
        time.sleep(2 + round(random.random(), 2))
    if i % 1000 == 0:
        print('已完成1000个')
    url = url.split('?')[0]

    if url in crawled_urls:
        # print('url已存在，跳过')
        skip_status = True
        continue

    try:
        resp = requests.get(url, headers=headers)
    except Exception as e:
        print(url)
        print(e)
        continue

    tree = etree.HTML(resp.content)

    # if tree.xpath('//div[@class="title"]//span')

    # 标题和关注数
    title_elem = tree.xpath(
        '//div[@data-component="detailHeader"]/div[@class="detailHeader VIEWDATA"]')
    title = etree.tostring(title_elem[0], method='html', encoding='utf-8').decode('utf-8')

    # 价格区域等
    try:
        overview_intro_elem = tree.xpath('//div[@data-component="overviewIntro"]//div[@class="content"]')
        overview_intro = etree.tostring(overview_intro_elem[0], method='html', encoding='utf-8').decode('utf-8')
    except IndexError:
        print(IndexError(url))

    # 基本信息
    m_content_elem = tree.xpath('//div[@class="m-content"]/div[@class="box-l"]')
    m_content = etree.tostring(m_content_elem[0], method='html', encoding='utf-8').decode('utf-8')

    try:
        c.execute("""INSERT INTO log(url, title, overview_intro, m_content) VALUES(%s, %s, %s, %s)"""
                  ,(url, title, overview_intro, m_content))
        conn.commit()
        print(f'爬取 {url} 成功！')
    except:
        print(url + ' insert wrong!!!')
        conn.rollback()
    skip_status = False

conn.close()
