import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

sessionid = sys.argv[1]

service = Service(executable_path='.\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

insta_url = 'https://www.instagram.com'
driver.get(insta_url)

time.sleep(1)

driver.delete_all_cookies()
driver.add_cookie({"name" : "sessionid", "value" : sessionid})
driver.refresh()

