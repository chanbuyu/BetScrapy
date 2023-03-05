import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def chrome_start():
    # 开启浏览器
    chrome = webdriver.Firefox()
    chrome.get('https://eosflare.io/whales')
    wait = WebDriverWait(chrome, 10)
    # 采用xpath监测数据是否加载出来
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="flex xs12 sm4 md3 lg2"]')))

    # 点击每页50按钮
    chrome.find_element(By.XPATH, '//div[@class="input-group__selections__comma"]').click()
    # 点击每页500按钮
    chrome.find_element(By.XPATH, '//div[@class="list__tile__title"][contains(text(),"500")]').click()
    # 延迟1秒，等待数据加载
    time.sleep(1)
    # 继续监测数据是否加载
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="flex xs12 sm4 md3 lg2"]')))

    # 处理数据
    while True:
        data_dispose(chrome)
        chrome.find_element(By.XPATH, '//div[@class="data-iterator__actions__range-controls"]/button[2]').click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="flex xs12 sm4 md3 lg2"]')))


def data_dispose(chrome):
    # 提取整行数据
    data = chrome.find_elements(By.XPATH, '//div[@class="container fluid grid-list-md"]/div[@class="layout row wrap"]')
    olist = []

    for d in data:
        olist.append(d.text)

    # 打开文件，将数据写入文件中
    with open("data.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(olist, ensure_ascii=False))
        f.write("\n")
    print("保存成功")


if __name__ == '__main__':
    # chrome_headless()
    chrome_start()
