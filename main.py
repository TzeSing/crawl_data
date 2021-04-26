# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

t0 = time.time()
options = Options()  # 实例化option对象
options.add_argument('--headless')  # 给option对象添加无头参
prefs = {
    'profile.managed_default_content_settings.images': 2,
    'permissions.default.stylesheet': 2
}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', options=options)
driver.get('https://www.baidu.com')

btn = driver.find_element_by_xpath('//*[@id="su"]')
print(btn.get_attribute('value'))

driver.close()

print(f'耗时: {time.time() - t0}')
