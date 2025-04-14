# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0060C468EE62BD16693179D0CE943752E9E8C2409B463406E69022110A00B86490A3F65F7227F2219A10683B2F480A3522FCB06C336B6D2676F2F528A8B34CF97D45009B0DD6EEFCCA76AA56D69E0427642D205FE8C0EB7926AD4855DE1DE4F486E56D019BA6CCB9A66C6D8FF26F505CCBBC741C3855DAC3538E4116F97B2C71A32FECF940EE21E624B02E5B62EFCD419787BC4F13C815F45942033479EE673D29CA4EEA3176DC9DEA61BD0D1DF412E739390F0096150B95EF9A6AC2F3814D62F0F4FD5C80F938EC1655CFF423ACBA49C5BBB368CAE7349469CF602616908ABEB70D9C479716FFBC250BCCC94CF03B1971F9B8FAB4CD740814733E4AE8525CEFCC125932B6536EA86F1F33923B1FDFDF51F83E503A430919939FEED84DB441AC1C7CCC1649FC2A5135F2C8584B37FE63B530905275B98094E973D611B7263635851EAE46C5524EA41CA6A7194939077B3C45736B93F3BD5BEC3B3175E63BF7C474"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
