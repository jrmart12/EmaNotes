from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

driver.get(os.environ.get('AcellusUrl'))

webhook = os.environ.get('WebhookUrlSlack')


def login_to_acellus():
    ID = os.environ.get('AcellusID')
    Password = os.environ.get('AcellusPassword')

    input_acellusID = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="AcellusID"]'))
    )
    input_acellusPassword = driver.find_element(By.XPATH, '//input[@name="Password"]')

    input_acellusID.send_keys(ID)
    input_acellusPassword.send_keys(Password)

    signInButton = driver.find_element(By.XPATH, '//input[@alt="Sign In"]')
    signInButton.click()


def score_tab_acellus():
    scoreButton = driver.find_element(By.XPATH, '//a[@href="score.html"]')
    scoreButton.click()

def retrieve_table_data():
    message = ""
    goals = ""
    rowcount = len(driver.find_elements(By.XPATH, '//table[@id="classList"]/tr'))
    columncount = len(driver.find_elements(By.XPATH, '//table[@id="classList"]/tr[1]/td'))
    first_part = '//table[@id="classList"]/tr['
    second_part = ']/td['
    third_part = ']'
    remove_special_lessons = '/span'
    i = '/i'

    for n in range(1, rowcount + 1):
        final_path = first_part + str(n) + second_part + str(6) + third_part
        table_data = driver.find_element_by_xpath(final_path).text
        if table_data == '100%':
            None
        else:
            for m in range(2, columncount + 1):
                if m == 2 :
                    final_path = first_part + str(n) + second_part + str(m) + third_part +remove_special_lessons
                    table_data = driver.find_element_by_xpath(final_path).text
                    message += table_data
                elif m == 3:
                    None
                elif m == 4:
                    final_path = first_part + str(n) + second_part + str(m) + third_part
                    table_data = driver.find_element_by_xpath(final_path).text
<<<<<<< HEAD
                    message += '   [Grade: ' + table_data + "]   "
=======
                    message += '   [Grade:' + table_data + "]   "
>>>>>>> 828e029bed7b1109fa7e44f745f79a66c61ef5b6
                elif m == 5:
                    final_path_for_i = first_part + str(n) + second_part + str(m) + third_part + i
                    try:
                        table_data = driver.find_element_by_xpath(final_path_for_i)
                        attribute = table_data.get_attribute('class')
                        if attribute == 'fa fa-star gold-star':
                            goals = ':thumbsup:'
<<<<<<< HEAD
                        elif attribute == 'fa fa-star gray-star':
=======
                        elif attribute == 'fa fa-star gold-star':
>>>>>>> 828e029bed7b1109fa7e44f745f79a66c61ef5b6
                            goals = ':thumbsdown:'
                    except NoSuchElementException:
                        goals = ':mortar_board:'
                    message += goals + "   "
                elif m == 6:
                    final_path = first_part + str(n) + second_part + str(m) + third_part
                    table_data = driver.find_element_by_xpath(final_path).text
                    message += '[' + table_data + "complete]   "
                else:
                    final_path = first_part + str(n) + second_part + str(m) + third_part
                    table_data = driver.find_element_by_xpath(final_path).text
                    message += table_data
            message += "\n"
    driver.quit()
    return message


def send_slack_message(message):
    payload = json.dumps(message)
    response = requests.post(webhook, data=payload)


login_to_acellus()
score_tab_acellus()
text = {
    "text": retrieve_table_data()
}
send_slack_message(text)