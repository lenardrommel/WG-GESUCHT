import json
import time
import datetime
import argparse
from numpy.random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import urllib.request

# Load access data from config JSON
with open('config.json') as f:
    config = json.load(f)
    pwd_id = config['email']
    pwd = config['password']

# Initialize the WebDriver
firefox_binary_path = '/Applications/Firefox.app/Contents/MacOS/firefox'
service = Service(executable_path='geckodriver')
options = Options()
options.binary_location = firefox_binary_path  # Set the path to the Firefox binary
driver = webdriver.Firefox(service=service, options=options)

def connected():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        print('There seems to be a problem with the internet connection, try again later.')
        return False


def click_cookies(driver):
    if not connected():
        return
    driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    time.sleep(2)
    try:
        driver.find_element(By.CLASS_NAME, "cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes").click()
        time.sleep(randint(1, 3))
        driver.find_element(By.LINK_TEXT, "Bitte loggen Sie sich hier ein.").click()
        time.sleep(1)
        driver.find_element(By.NAME, "login_email_username").click()
        driver.find_element(By.ID, "login_email_username").send_keys(pwd_id)
        driver.find_element(By.NAME, "login_password").click()
        driver.find_element(By.NAME, "login_password").send_keys(pwd)
        driver.find_element(By.ID, "login_submit").click()
        driver.minimize_window()
    except NoSuchElementException:
        print("Could not find an element during the login process.")
        driver.quit()


def is_webdriver_alive(driver):
    print('Checking whether the driver is alive')
    try:
        assert(driver.service.process.poll() is None)  # Returns an int if dead and None if alive
        driver.service.assert_process_still_running()  # Throws a WebDriverException if dead
        driver.find_element(By.TAG_NAME, 'html')  # Throws a NoSuchElementException if dead
        print('The driver appears to be alive')
        return True
    except (NoSuchElementException, WebDriverException, AssertionError):
        print('The driver appears to be dead')
        return False
    except Exception as ex:
        print(f'Encountered an unexpected exception type ({type(ex)}) while checking the driver status')
        return False


def error_exit():
    print('Element could not be found. Try again.')
    try:
        driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    except:
        print('Could not open the browser.')
    time.sleep(randint(2, 4))


def exit_script():
    if connected():
        driver.get('https://www.wg-gesucht.de/meine-anzeigen.html')
    time.sleep(randint(1, 6))


def update_wgg(wait_time):
    time.sleep(2)
    try:
        driver.find_element(By.CLASS_NAME, "mdi.mdi-dots-vertical.mdi-20px.pull-right.cursor-pointer").click()
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Bearbeiten + Fotos").click()
        time.sleep(wait_time)
        driver.find_element(By.ID, "update_offer_nav").click()
        time.sleep(2)
    except NoSuchElementException:
        error_exit()

    exit_script()


def main(debug=False):
    wait_time = 5 if debug else randint(1, 4) * 9
    click_cookies(driver)
    while True:
        if connected():
            update_wgg(wait_time)
            print('Last actualization at', datetime.datetime.today())
            time.sleep(5 if debug else 300)
            time.sleep(5 if debug else int(randint(1, 10) * 30))
        else:
            while not connected():
                time.sleep(5 if debug else 45 * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WG-Gesucht Update Script")
    parser.add_argument('--debug', action='store_true', help="Run in debug mode with reduced waiting times")
    args = parser.parse_args()

    try:
        main(debug=args.debug)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("Script finished")