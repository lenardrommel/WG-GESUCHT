from numpy import random
import numpy as np
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


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


def reopenBrowser():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    update_wgg()


def errorExit():
    print('Element could not be found. Try again.')
    try:
        driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    except:
        reopenBrowser()
    time.sleep(random.randint(2, 4))


def exit():
    driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    time.sleep(random.randint(1, 6))


def update_wgg():
    time.sleep(1)
    try:
        driver.find_element(By.CLASS_NAME, "mdi.mdi-dots-vertical.mdi-20px.pull-right.cursor-pointer").click()
        time.sleep(10)
    except NoSuchElementException:
        errorExit()
    try:
        driver.find_element(By.LINK_TEXT, "Bearbeiten + Fotos").click()
        time.sleep(random.randint(1, 4) * 9)
    except NoSuchElementException:
        errorExit()
    try:
        driver.find_element(By.ID, "update_offer_nav").click()
        time.sleep(10)
    except:
        errorExit()

    exit()


def answer(): # not nearly finished
    driver.get('https://www.wg-gesucht.de/nachrichten.html')
    try:
        driver.find_element(By.CLASS_NAME, 'panel-body conversation_selected conversation_unread').click()
    except:
        driver.find_element(By.CLASS_NAME, 'panel-body conversation_selected ').click()
    
    


while True:
    update_wgg()
    print('Last actualization at', time.localtime()[3], 'h', time.localtime()[4], 'min')
    with open("log/log.txt", "a") as f:
        print(int(time.localtime()[3]), int((time.localtime()[4])), file=f)
    time.sleep(20)
    