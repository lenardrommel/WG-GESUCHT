from numpy import random
import numpy as np
import pandas as pd
import urllib.request
import time
import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait




# define access data
pwd_id = np.loadtxt('../alt/user_data.csv', dtype='str')[0]
pwd = np.loadtxt('user_data.csv', dtype='str')[1]



driver = webdriver.Firefox(executable_path='geckodriver')
#driver.maximize_window()


def click_cookies(driver):
    if not connected():
        return
    driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes").click()
    time.sleep(random.randint(1, 3))
    driver.find_element(By.LINK_TEXT, "Bitte loggen Sie sich hier ein.").click()
    time.sleep(1)
    driver.find_element(By.NAME, "login_email_username").click()  # "form-control.wgg_input"
    driver.find_element(By.ID, "login_email_username").send_keys(pwd_id)
    driver.find_element(By.NAME, "login_password").click()
    driver.find_element(By.NAME, "login_password").send_keys(pwd)
    driver.find_element(By.ID, "login_submit").click()
    driver.minimize_window()


def connected():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        print('There seems to be a problem with the internet connection, try again later.')
        return False


def is_webdriver_alive(driver):
    print('Checking whether the driver is alive')
    '''if not connected():
        print('There is no connection to the internet.')
        return False'''
    try:
        assert(driver.service.process.poll() == None) #Returns an int if dead and None if alive
        driver.service.assert_process_still_running() #Throws a WebDriverException if dead
        driver.find_element_by_tag_name('html') #Throws a NoSuchElementException if dead
        print('The driver appears to be alive')
        return True
    except (NoSuchElementException, WebDriverException, AssertionError):
        print('The driver appears to be dead')
        return False
    except Exception as ex:
        print('Encountered an unexpected exception type ({}) while checking the driver status'.format(type(ex)))
        return False

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
    if connected():
        driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    time.sleep(random.randint(1, 6))


def update_wgg():
    time.sleep(2)
    try:
        driver.find_element(By.CLASS_NAME, "mdi.mdi-dots-vertical.mdi-20px.pull-right.cursor-pointer").click()
        time.sleep(2)
    except NoSuchElementException:
        errorExit()
    try:
        driver.find_element(By.LINK_TEXT, "Bearbeiten + Fotos").click()
        time.sleep(random.randint(1, 4) * 9)
    except NoSuchElementException:
        errorExit()
    try:
        driver.find_element(By.ID, "update_offer_nav").click()
        time.sleep(2)
    except:
        errorExit()

    exit()


def answer(): # not nearly finished
    driver.get('https://www.wg-gesucht.de/nachrichten.html')
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'conversation_list_item')))
    conversations = driver.find_elements(By.CLASS_NAME, 'conversation_list_item')
    for x in conversations:
            x.click()
            time.sleep(3)
            message = driver.find_element(By.CLASS_NAME, 'row last_message_selector')
            #wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'message_content message_text')))
            print('True')
    
    

click_cookies(driver)
prev = np.loadtxt('log/log.txt', dtype=str)
print(f'Previous actualization was at {prev[-1]}')
while True:
    if connected():
        update_wgg()
        print('Last actualization at', datetime.datetime.today())

        with open("log/log.txt", "a") as f:
            print(datetime.datetime.today(), file=f)
            time.sleep(300)
            time.sleep(int(random.uniform(1, 10) * 30))
    else:
        while not connected():
            time.sleep(45 * 60)
    