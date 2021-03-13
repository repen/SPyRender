from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
import os, time
from config import BASE_DIR

def init_driver(headless=False):
    co = Options()
    # co.add_argument('user-agent={}'.format(userAgent))
    if headless:
        co.add_argument('--headless')
        co.add_argument('--no-sandbox')
        co.add_argument('--disable-dev-shm-usage')
        co.add_argument("--mute-audio")
        # disable infobars
        co.add_argument('--disable-infobars')

    co.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    co.add_experimental_option("prefs", chrome_prefs)
    driver = webdriver.Chrome(chrome_options=co)
    return driver

if __name__ == '__main__':
    driver = init_driver( headless=False )
    try:
        driver.get("https://ya.ru")
        time.sleep(15)
    finally:
        driver.quit()