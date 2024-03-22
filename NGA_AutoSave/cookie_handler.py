import os
import pickle
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 测试链接
url = 'https://bbs.nga.cn/read.php?tid=10862033'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/120.0.0.0 Safari/537.36'
           }

session = requests.Session()


def get_cookie():
    # 得到Cookie的字符串
    if not is_cookie_expired():
        return read_cookie()
    else:
        return save_cookie()


def read_cookie():
    # 从本地文件中读取 cookie 对象
    if not os.path.exists(r'Settings/cookie.pkl'):
        return ""
    with open(r'Settings/cookie.pkl', 'rb') as file:
        cookie = pickle.load(file)
        return cookie


def save_cookie():
    # 将 cookie 写入本地文件,并返回
    cookie_str = ''
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")  # 禁用弹窗拦截
    driver = uc.Chrome(options=options)
    driver.get(url)
    WebDriverWait(driver, 1000, 1).until(EC.visibility_of_element_located((By.ID, 'postauthor0')))
    cookie_list = driver.get_cookies()
    driver.close()
    for cookie in cookie_list:
        cookie_str += f'{cookie["name"]}={cookie["value"]}; '
    with open(r'Settings/cookie.pkl', 'wb') as file:
        pickle.dump(cookie_str, file)
    return cookie_str


def is_cookie_expired():
    # 判断Cookie是否过期
    cookie = read_cookie()
    headers['Cookie'] = cookie
    re = session.get(url, headers=headers)
    if re.status_code == 200:
        return False
    else:
        return True



