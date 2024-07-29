import json
import os.path

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
import logging

logger = logging.getLogger(__name__)


class TelegramAccount:
    # dogs_url = "https://web.telegram.org/a/#7352918101"
    base_url = "https://web.telegram.org"

    def __init__(self, account_name):
        os.makedirs("sessions", exist_ok=True)


        # Initialize Firefox Profile
        # profile = FirefoxProfile()
        # # profile.set_preference("dom.serviceWorkers.enabled", True)
        # # profile.set_preference("dom.serviceWorkers.openWindow.enabled", True)
        # # profile.set_preference("dom.webnotifications.serviceworker.enabled", True)
        # # profile.set_preference("dom.caches.enabled", True)
        # # profile.set_preference("dom.push.enabled", True)
        # # profile.set_preference("dom.serviceWorkers.interception.enabled", True)
        # profile.set_preference("useAutomationExtension", False)
        # #
        # # Initialize Firefox Options
        # options = Options()
        # options.profile = profile
        # options.set_preference("dom.webdriver.enabled", False)
        # options.add_argument("-private")  # Start Firefox in private mode
        # options.add_argument("--headless")  # Optional: run in headless mode

        #
        #
        # service = FirefoxService(executable_path='/usr/local/bin/geckodriver')
        self.driver = webdriver.Firefox()
        self.account_name = account_name
        self.fetch_account()

    def save_state(self):
        time.sleep(10)
        cookies = self.driver.get_cookies()
        print(cookies, len(cookies))
        print(len(cookies))
        with open(os.path.join("sessions", f'{self.account_name}_cookies.pkl'), 'wb') as file:
            pickle.dump(cookies, file)
        local_storage = self.driver.execute_script("return window.localStorage;")
        with open(os.path.join("sessions", f'{self.account_name}_local_storage.json'), 'w')as file:
            json.dump(local_storage, file)

    def login(self):
        # Go to login page
        self.driver.get(self.base_url)

        input("Type any key, when login finished:")
        self.save_state()
        logger.info(f"Logged into Telegram Account: {self.account_name}")

    def fetch_account(self):
        logger.info(f"fetching account {self.account_name} data")
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
            logger.info(f"No session data for {self.account_name}, log in manually.")
            self.login()

    def claim(self):
        dogs_url = "https://web.telegram.org/k/#@dogshouse_bot"
        self.driver.get(dogs_url)
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".new-message-bot-commands").click()
        self.driver.find_element(By.XPATH, "/html/body/div[7]/div/div[2]/button[1]").click()
        time.sleep(5)
        self.driver.switch_to.frame(0)
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".\\_root_oar9p_1").click()
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".\\_root_oar9p_1").click()
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".\\_root_oar9p_1").click()
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".\\_root_oar9p_1").click()


        # self.driver.find_element(By.CSS_SELECTOR, "._root_oar9p_1").click()
        # time.sleep(10)
        # self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]").click()
        # time.sleep(3)
        # time.sleep(3)
        # self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[8]").click()
        #
        # self.driver.switch_to.frame(0)
        # self.driver.find_element(By.CSS_SELECTOR, ".\\_listItem_1wi4k_1:nth-child(2) .\\_root_oar9p_1").click()
        # print(self.driver.current_url)
        logger.info(f"Successfully claimed for {self.account_name}")

    def close(self):
        self.driver.quit()

