import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

HEADERS = {
    'referer': 'https://ys.mihoyo.com/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'cookie': 'UM_distinctid=175e36c178da74-072452c0a3c471-3a7b035f-1fa400-175e36c178ec68'
}
BASE_FOLDER = '/home/lizhe/Pictures/genshin'
BASE_URL = 'https://ys.mihoyo.com/main/manga/detail/184?mute=1'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('/home/lizhe/chromedriver', chrome_options=chrome_options)
    return driver


def get_images(driver, folder):
    # 获取所有图片元素
    imgs = driver.find_elements_by_xpath("//div[@class='viewer']//img")
    n = 1
    while n < len(imgs)+1:
        # 前三张通常是src中有url，后面通常是data-src中有url
        src = imgs[n-1].get_attribute('src')
        if not src:
            src = imgs[n-1].get_attribute('data-src')
        print(src)
        image_content = requests.get(url=src, headers=HEADERS)
        # 拿到图片扩展名，存储
        tail = str(src).split('.')[-1]
        with open(folder + '/' + '{:04}'.format(n) + '.' + tail, 'wb') as f:
            f.write(image_content.content)
        time.sleep(1)
        n += 1

def main():
    driver = get_driver()
    driver.get(BASE_URL)
    time.sleep(2)
    # 先算出所有章节数
    options = driver.find_elements_by_xpath("//select[@class='bottombar__chapter']/option")
    chapter_nums = len(options)
    for i in range(chapter_nums):
        # 每次轮询需要重新获取select elements，否则会报错
        options = driver.find_elements_by_xpath("//select[@class='bottombar__chapter']/option")
        options[i].click()
        time.sleep(2)
        print(options[i].text)
        dirname = BASE_FOLDER + '/' + options[i].text
        os.makedirs(dirname, exist_ok=True)
        get_images(driver, dirname)


if __name__ == '__main__':
    main()
    pass
