from numpy import random
import numpy as np
import urllib.request
import time
import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait


class Bot():
    def __init__(self, mode, season, waittime, pwd_id, pwd):
        super(Bot, self).__init__()
        self.mode = mode
        self.season = season
        self.waittime = waittime
        self.driver = webdriver.Firefox(executable_path='geckodriver')
        self.pwd_id = pwd_id
        self.pwd = pwd

        if mode == 'test':
            self.waittime = 1


    def click_cookies(self):
        self.driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
        time.sleep(1)
        self.driver.find_element(By.CLASS_NAME, 'cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Bitte loggen Sie sich hier ein.").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, "login_email_username").click()
        self.driver.find_element(By.ID, "login_email_username").send_keys(self.pwd_id)
        self.driver.find_element(By.NAME, "login_password").click()
        self.driver.find_element(By.NAME, "login_password").send_keys(self.pwd)
        self.driver.find_element(By.ID, "login_submit").click()
        self.driver.minimize_window()

    def connected(self):
        try:
            urllib.request.urlopen('http://google.com')
            return True
        except:
            print('There seems to be a problem with the internet connection, try again later.')
            return False

    def reopenBrowser(self):
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
        time.sleep(1)

    def update(self):

        self.driver.find_element(By.CLASS_NAME, "mdi.mdi-dots-vertical.mdi-20px.pull-right.cursor-pointer").click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Bearbeiten + Fotos").click()
        time.sleep(random.randint(1, 4) * self.waittime)
        self.driver.find_element(By.ID, "update_offer_nav").click()
        print(f'Updated successfully at {datetime.datetime.today()}.')
        time.sleep(2)





pwd_id = np.loadtxt('user_data.csv', dtype='str')[0]
pwd = np.loadtxt('user_data.csv', dtype='str')[1]
bot = Bot(mode=True, season=True, waittime=1, pwd_id=pwd_id, pwd=pwd)
bot.click_cookies()
while True:
    bot.update()
    print('hello')