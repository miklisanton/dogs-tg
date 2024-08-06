import json
import os.path
from seleniumwire import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
import logging
import re

logger = logging.getLogger(__name__)


class TelegramAccount:
    # dogs_url = "https://web.telegram.org/a/#7352918101"
    base_url = "https://web.telegram.org"

    def __init__(self, account_name):
        self.account_name = account_name
        os.makedirs("sessions", exist_ok=True)
        options = Options()
        #options.add_argument("--headless=new")

        # proxy_url = "http://Hx2o10:UcuCR2@45.83.11.10:8000"
        proxy_url = self.get_proxy()
        if proxy_url == "-":
            seleniumwire_options = None
        else:
            seleniumwire_options = {
                "proxy": {
                    "http": proxy_url,
                    "https": proxy_url
                },
            }

        self.driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options)
        self.fetch_account()

    def get_proxy(self):
        try:
            with open(os.path.join("sessions", f'{self.account_name}_proxy.txt'), 'r') as file:
                proxy = file.readline()
                return proxy
        except FileNotFoundError:
            # Request proxy from stdin until valid
            proxy_pattern = re.compile(r'^http://(?:\S+:\S+@)?\S+:\d+$')
            while True:
                proxy = input("Enter a proxy (format: http://username:password@host:port) or - to avoid proxy: ")
                if proxy == "-" or re.match(proxy_pattern, proxy) is not None:
                    print(f"Valid proxy entered: {proxy}")
                    with open(os.path.join("sessions", f'{self.account_name}_proxy.txt'), 'w') as file:
                        file.write(proxy)
                    return proxy
                else:
                    print("Invalid proxy format. Please try again.")

    def save_state(self):
        time.sleep(10)
        cookies = self.driver.get_cookies()
        print(cookies, len(cookies))
        print(len(cookies))
        with open(os.path.join("sessions", f'{self.account_name}_cookies.pkl'), 'wb') as file:
            pickle.dump(cookies, file)
        local_storage = self.driver.execute_script("return window.localStorage;")
        with open(os.path.join("sessions", f'{self.account_name}_local_storage.json'), 'w') as file:
            json.dump(local_storage, file)

    def login(self):
        # Go to login page
        self.driver.get(self.base_url)

        input("Type any key, when login finished:")
        self.save_state()
        logger.warning(f"Logged into Telegram Account: {self.account_name}")

    def fetch_account(self):
        logger.warning(f"fetching account {self.account_name} data")
        try:
            self.driver.get(self.base_url)
            with open(os.path.join("sessions", f'{self.account_name}_cookies.pkl'), 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            with open(os.path.join("sessions", f'{self.account_name}_local_storage.json'), 'r') as file:
                local_storage = json.load(file)
                for key, value in local_storage.items():
                    self.driver.execute_script(f"window.localStorage.setItem(arguments[0], arguments[1]);", key, value)
            self.driver.refresh()
        except FileNotFoundError:
            logger.warning(f"No session data for {self.account_name}, log in manually.")
            self.login()

    def claim_dogs(self):
        dogs_url = "https://web.telegram.org/k/#@dogshouse_bot"
        self.driver.get(dogs_url)
        time.sleep(15)
        self.driver.find_element(By.CSS_SELECTOR, ".new-message-bot-commands").click()
        self.driver.find_element(By.XPATH, "/html/body/div[7]/div/div[2]/button[1]").click()
        time.sleep(5)
        self.driver.switch_to.frame(0)
        time.sleep(10)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[8]").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[8]").click()

        logger.warning(f"Successfully claimed for {self.account_name}")

    def claim_hot(self):
        hot_url = "https://web.telegram.org/k/#@herewalletbot"
        self.driver.get(hot_url)
        time.sleep(1000)
        self.driver.find_element(By.CSS_SELECTOR, ".bubbles-group:nth-child(9) .reply-markup-row:nth-child(3) .c-ripple").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, "/html/body/div[7]/div/div[2]/button[1]").click()
        # login

        # login end
        time.sleep(5)
        self.driver.switch_to.frame(0)
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div > svg").click()
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".sc-dJDBYC").click()

        logger.warning(f"Successfully claimed for {self.account_name}")


    def close(self):
        self.driver.quit()
