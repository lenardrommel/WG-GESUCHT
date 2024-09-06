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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request


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


def wait_for_element(driver, by, value, timeout=20, retries=3):
    while retries > 0:
        try:
            element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            retries -= 1
            print(f"Retry {3 - retries}: Element {value} not found. Retrying...")
            time.sleep(2)  # Wait before retrying
    print(f"Failed to find element {value} after several retries.")
    return None


def incremental_sleep_check(driver, check_function, max_wait_time=20, initial_sleep=2, increment_sleep=5):
    total_sleep = 0
    while total_sleep < max_wait_time:
        if check_function(driver):
            return True
        time.sleep(initial_sleep)
        total_sleep += initial_sleep
        initial_sleep = increment_sleep  # Increase sleep time after the first check
    return False


def element_available(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False


def click_cookies(driver, pwd_id, pwd):
    if not connected():
        return False
    try:
        driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')

        if not incremental_sleep_check(driver, lambda d: element_available(d, By.CLASS_NAME,
                                                                           "cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes")):
            print("Cookies button not available after waiting.")
            return False

        driver.find_element(By.CLASS_NAME, "cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes").click()

        if not incremental_sleep_check(driver,
                                       lambda d: element_available(d, By.LINK_TEXT, "Bitte loggen Sie sich hier ein.")):
            print("Login link not available after waiting.")
            return False

        driver.find_element(By.LINK_TEXT, "Bitte loggen Sie sich hier ein.").click()

        if not incremental_sleep_check(driver, lambda d: element_available(d, By.NAME, "login_email_username")):
            print("Email field not available after waiting.")
            return False

        driver.find_element(By.NAME, "login_email_username").send_keys(pwd_id)

        if not incremental_sleep_check(driver, lambda d: element_available(d, By.NAME, "login_password")):
            print("Password field not available after waiting.")
            return False

        driver.find_element(By.NAME, "login_password").send_keys(pwd)

        if not incremental_sleep_check(driver, lambda d: element_available(d, By.ID, "login_submit")):
            print("Submit button not available after waiting.")
            return False

        driver.find_element(By.ID, "login_submit").click()
        driver.minimize_window()
        return True
    except (NoSuchElementException, WebDriverException) as e:
        print(f"Error during login process: {e}")
        return False


def update_wgg(driver, wait_time):
    if not incremental_sleep_check(driver, lambda d: element_available(d, By.CLASS_NAME,
                                                                       "mdi.mdi-dots-vertical.mdi-20px.pull-right.cursor-pointer")):
        print("Dots button not available after waiting.")
        return False

    driver.find_element(By.CLASS_NAME, "mdi.mdi-dots-vertical.mdi-20px.pull-right.cursor-pointer").click()

    if not incremental_sleep_check(driver, lambda d: element_available(d, By.LINK_TEXT, "Bearbeiten + Fotos")):
        print("Edit link not available after waiting.")
        return False

    driver.find_element(By.LINK_TEXT, "Bearbeiten + Fotos").click()
    time.sleep(wait_time)

    if not incremental_sleep_check(driver, lambda d: element_available(d, By.ID, "update_offer_nav")):
        print("Update button not available after waiting.")
        return False

    driver.find_element(By.ID, "update_offer_nav").click()

    # Assuming the window appears now, and you need to close it
    if incremental_sleep_check(driver, lambda d: element_available(d, By.CLASS_NAME, "modal-body")):
        driver.find_element(By.CLASS_NAME, "modal-body").click()
        time.sleep(2)  # Give it a moment to close the popup

    return True


def main(debug=False):
    pwd_id, pwd = load_config()
    wait_time = 5 if debug else randint(1, 4) * 9

    while True:
        driver = initialize_driver()
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
    parser.add_argument('--debug', action='store_true', help="Run in debug mode with reduced waiting times")
    args = parser.parse_args()

    try:
        main(debug=args.debug)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Script finished")
        exit()
