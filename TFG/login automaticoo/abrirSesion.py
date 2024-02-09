import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

sessionid = sys.argv[1]

# Configurar el servicio de ChromeDriver
service = Service(executable_path='.\chromedriver.exe')

# Configurar las opciones del navegador Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Crear una instancia del navegador Chrome
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Abrir la URL de Instagram
insta_url = 'https://www.instagram.com'
driver.get(insta_url)

time.sleep(1)
# Establecer la cookie

driver.delete_all_cookies()

driver.add_cookie({"name" : "sessionid", "value" : sessionid})

# Recargar la página para que la cookie tenga efecto
driver.refresh()

