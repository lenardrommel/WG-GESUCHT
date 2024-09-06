import json
import time
import datetime
import argparse
from numpy.random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import urllib.request

'''
This script currently has the feature that it reopens the browser every time there is a critical error.
'''


def load_config():
    try:
        with open('config.json') as f:
            config = json.load(f)
        return config['email'], config['password']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        exit()

def initialize_driver():
    try:
        firefox_binary_path = '/Applications/Firefox.app/Contents/MacOS/firefox'
        service = Service(executable_path='geckodriver')
        options = Options()
        options.binary_location = firefox_binary_path  # Set the path to the Firefox binary
        driver = webdriver.Firefox(service=service, options=options)
        return driver
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        exit()

def connected():
    try:
        urllib.request.urlopen('http://google.com', timeout=5)
        return True
    except:
        print('There seems to be a problem with the internet connection, try again later.')
        return False

def click_cookies(driver, pwd_id, pwd):
    if not connected():
        return False
    try:
        driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
        time.sleep(2)
        try:
            driver.find_element(By.CLASS_NAME, "cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes").click()
        except NoSuchElementException:
            print("Cookies button not found.")
        time.sleep(randint(1, 3))
        driver.find_element(By.LINK_TEXT, "Bitte loggen Sie sich hier ein.").click()
        time.sleep(1)
        driver.find_element(By.NAME, "login_email_username").send_keys(pwd_id)
        driver.find_element(By.NAME, "login_password").send_keys(pwd)
        driver.find_element(By.ID, "login_submit").click()
        return True
    except (NoSuchElementException, WebDriverException) as e:
        print(f"Error during login process: {e}")
        return False

def update_wgg(driver, wait_time):
    time.sleep(5)
    try:
        driver.find_element(By.CLASS_NAME, "mdi.mdi-dots-vertical.mdi-20px.pull-right.cursor-pointer").click()
        time.sleep(5)
        driver.find_element(By.LINK_TEXT, "Bearbeiten + Fotos").click()
        time.sleep(wait_time)
        driver.find_element(By.ID, "update_offer_nav").click()
        time.sleep(5)
        # Assuming the window appears now, and you need to close it

        try:
            # Click on an area outside the popup, e.g., the body or header
            driver.find_element(By.CLASS_NAME, "modal-body").click()
            time.sleep(5)  # Give it a moment to close the popup
        except NoSuchElementException:
            print("Could not find an element to close the popup. Continuing...")

        return True
    except NoSuchElementException as e:
        print(f"Update process failed: {e}")
        return False

def main(debug=False):
    pwd_id, pwd = load_config()
    wait_time = 5 if debug else randint(1, 4) * 9

    while True:
        driver = initialize_driver()
        if not debug:
            driver.minimize_window()
        try:
            if not click_cookies(driver, pwd_id, pwd):
                raise Exception("Failed during cookie and login process.")

            if not update_wgg(driver, wait_time):
                raise Exception("Failed during update process.")

            print('Last actualization at', datetime.datetime.today())
            time.sleep(5 if debug else 300)
            time.sleep(5 if debug else int(randint(1, 10) * 30))

        except Exception as e:
            print(f"An error occurred: {e}. Restarting the browser and process.")
            driver.quit()
            time.sleep(5)  # Wait a few seconds before retrying

        finally:
            driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WG-Gesucht Update Script")
    parser.add_argument('--debug', action='store_true', help="Run in debug mode with reduced waiting times", default=True)
    args = parser.parse_args()

    try:
        main(debug=args.debug)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Script finished")
        exit()