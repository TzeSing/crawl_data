# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

option = Options()  # 实例化option对象
option.add_argument("--headless")  # 给option对象添加无头参

driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', options=option)
driver.get('https://www.baidu.com')

btn = driver.find_element_by_xpath('//*[@id="su"]')
print(btn.get_attribute('value'))

driver.close()
