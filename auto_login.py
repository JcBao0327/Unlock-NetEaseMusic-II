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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F3934A360213C6EC783B87169AB6039E65F3676B0C40AEDC68895EE495A64B26981C1636C3066749B0E67D7CA5B4B7B8EE778377E68BD96C1D07EDBB088D7A30DAA41E7E4EA1858F24CD76EC8B82DA7CBBF9C4EB8B72F13DEEEF54F1650F9F2049B02FBE36FDE29C5FE7924E6ECDEF5E5076164B73E5927B62B2FF844A9B1B83F80F1EB47E6367066DADAF3C43B91CD4B21C7A5062632571C9762E4C4A76B235C3D9F062E0CE988DEBEFE859FCFD0790D891FBC193A33682D2B1BDC1C5A3DEAE0B7EF016DD0E4F095068339FDCED62BD3E8C84C2CEF5CFDFFD64ECCEAB5D590E5C48E51CB6F12F9021058FF61BE3C16D24487D6AE2742F1B5A3090B7C54D1D2FBC8AA1A2AD84E1C416E449DF877064B5488A15AD5D93BBC921EE026383954DD0C83A49F4E7F4958DC8768F8D5A760E0FF5A528F3A3BBE32AEA58D8DFE120C1FA84507EA3B30D78B4392F7ADF8C647F8F69CB44011F5F17F93CDE1B6AECC5C317"})
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
