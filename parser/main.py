import urllib3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from utils import load_file, load_json, parse_images


driver = webdriver.Chrome()

driver.get("https://drtechno.ru/?page=product")
wait = WebDriverWait(driver, 10)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# load_file(wait, driver)

# load_json(wait, driver)

parse_images(wait, driver)

driver.quit()