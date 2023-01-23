from numpy import random
import numpy as np
import time
from selenium.webdriver.common.by import By
from selenium import webdriver


# define access data
pwd_id = np.loadtxt('user_data.csv', dtype='str')[0]
pwd = np.loadtxt('user_data.csv', dtype='str')[1]


driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
time.sleep(2)
driver.find_element(By.CLASS_NAME, "cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes").click()
time.sleep(random.randint(1, 3))
driver.find_element(By.LINK_TEXT, "Bitte loggen Sie sich hier ein.").click()
time.sleep(1)
driver.find_element(By.NAME, "login_email_username").click() # "form-control.wgg_input"
driver.find_element(By.ID, "login_email_username").send_keys(pwd_id)
driver.find_element(By.NAME, "login_password").click()
driver.find_element(By.NAME, "login_password").send_keys(pwd)
driver.find_element(By.ID, "login_submit").click()
time.sleep(1)


def update_wgg():
    driver.find_element(By.CLASS_NAME, "mdi.mdi-dots-vertical.mdi-20px.pull-right.cursor-pointer").click()
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, "Bearbeiten + Fotos").click()
    time.sleep(random.randint(1, 4))
    driver.find_element(By.ID, "update_offer_nav").click()
    time.sleep(30)
    driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    time.sleep(random.randint(1, 6) * 10)


def answer():
    driver.get('https://www.wg-gesucht.de/nachrichten.html')



while True:
    update_wgg()
    time.sleep(4)
    print(time.time())