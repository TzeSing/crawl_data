# -*- coding: utf-8 -*-
"""requests爬取所有链接，然后再分批爬取链接里的内容
"""
import json
import random
import time

import requests
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'lianjia_uuid=134c13b6-6255-4895-9f81-7c6df0dce4ce; sajssdk_2015_cross_new_user=1; select_city=440100; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1619420240,1619423337; _smt_uid=60867371.535bd856; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221790cf76bee71b-00b8a87eec5642-3f356b-2073600-1790cf76befcc7%22%2C%22%24device_id%22%3A%221790cf76bee71b-00b8a87eec5642-3f356b-2073600-1790cf76befcc7%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyguangzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; lianjia_ssid=6ffe4e6d-7151-4d2d-a42d-eae9452de871; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1619428265; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYzE2OTlhMTMxZTA3OGFhNTJjMGJlNWM4OTE0NDc5ZWNkMzYwNzQ0M2U3MzU2NWY5MDRkMTE5ZGFlMjFhMTM2YWRjMTQyYzgxMGRhN2RkMzAxMDA1YmIyYzZmNjU4Yjg0ZmMzMGU4NTkwZjEzZDc3MzZmNmQ1M2E2MDc0ZDEwMmY1YzNjYjk1NWNiNTA1OTNmYTRlMmY4NDYyN2IzMDEwZGFjZWM1N2VhOGNlOGE5MDJjZDkzYzNmOWUzMzgzMWZhNDc0MWQ3OGFjNTgwNjYzMTUzN2U4MDc0MmJmZjk5MWQ1ZDEzMWY0Zjg3N2NlMjRmNWU1ZTFlOTNlNjQ0ODFhYjkyZWMxOWRhNjlkZjIyMGMxZWI5NzQ4OGQ4MzQ4OTE0YWI2OTA4NzlmNmJmODRhYmRiYmNlYjkzZGQ0ZmRjM2VmNjk5ZWI0YmRkODNmYmI2NjFkYTA4ZjcwMmQ1NGExZlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI4NjQ3OTViMVwifSIsInIiOiJodHRwczovL2d6LmtlLmNvbS9lcnNob3VmYW5nL2RvbmdzaGFua291LyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9',
    'Host': 'gz.ke.com',
    'Pragma': 'no-cache',
    'Referer': 'https://gz.ke.com/ershoufang/dongfengdong/pg6/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

distinct_urls = ['https://gz.ke.com/ershoufang/tianhe/',
                 'https://gz.ke.com/ershoufang/yuexiu/',
                 'https://gz.ke.com/ershoufang/liwan/',
                 'https://gz.ke.com/ershoufang/haizhu/',
                 'https://gz.ke.com/ershoufang/panyu/',
                 'https://gz.ke.com/ershoufang/baiyun/',
                 'https://gz.ke.com/ershoufang/huangpugz/',
                 'https://gz.ke.com/ershoufang/conghua/',
                 'https://gz.ke.com/ershoufang/zengcheng/',
                 'https://gz.ke.com/ershoufang/huadou/',
                 'https://gz.ke.com/ershoufang/nansha/',
                 'https://gz.ke.com/ershoufang/nanhai/',
                 'https://gz.ke.com/ershoufang/shunde/'
                 ]

with open('urls.txt', 'r') as f:
    area_urls = f.read().split('\n')

# 获取各区下面的区域url
# with open('urls.txt', 'w', encoding='utf-8') as f:
#     for url in distinct_urls:
#         time.sleep(2 + round(random.random(), 2))
#         resp = requests.get(url, headers=headers)
#         tree = etree.HTML(resp.content)
#         urls = tree.xpath('//*[@id="beike"]//dd//*[@data-role="ershoufang"]/div[2]/a/@href')
#         for u in urls:
#             f.write(f'https://gz.ke.com{u}\n')

# 获取各区域下的页数
with open('url_with_num.txt', 'w', encoding='utf-8') as f:
    for url in area_urls:
        time.sleep(2 + round(random.random(), 2))
        resp = requests.get(url, headers=headers)
        tree = etree.HTML(resp.content)
        try:
            page = tree.xpath('//*[@comp-module="page"]/@page-data')[0]
            total_page = json.loads(page)['totalPage']
            f.write(f'{url} {total_page}\n')
        except:
            print(url)
            print(tree.xpath('//*[@comp-module="page"]/@page-data'))
            print()

