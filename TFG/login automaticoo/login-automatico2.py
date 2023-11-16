from selenium import webdriver
import sys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

# Obtener el nombre de usuario y contraseña de los argumentos de línea de comandos
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
SECURITYCODE = '11111'  # Valor por defecto

# Configurar el servicio de ChromeDriver
service = Service(executable_path='.\chromedriver.exe')

# Configurar las opciones del navegador Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Crear una instancia del navegador Chrome
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Abrir la URL de Instagram
insta_url = 'https://www.instagram.com/accounts/login/'
driver.get(insta_url)

# Esperar y hacer clic en el botón de cookies
cookies_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]')))
cookies_button[0].click()

# Esperar y ingresar el nombre de usuario y contraseña
username_field = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.NAME, 'username')))
username_field[0].send_keys(USERNAME)

password_field = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.NAME, 'password')))
password_field[0].send_keys(PASSWORD)

# Hacer clic en el botón de inicio de sesión
login_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]')))
login_button[0].click()



# Establecer un tiempo máximo de espera de 2 minutos
file_path = f"../../../codigos/{USERNAME}.txt"
start_time = time.time()
while not os.path.exists(file_path) and time.time() - start_time < 120:
    time.sleep(1)
    

if os.path.exists(file_path):
    # Archivo encontrado, leer su contenido y almacenarlo en la variable SECURITYCODE
    with open(file_path, 'r') as file:
        SECURITYCODE = file.read().strip()
else:
    # Se ha alcanzado el tiempo máximo de espera, maneja el caso en el que el archivo no apareció
    print("Archivo no encontrado dentro del tiempo máximo de espera.")
   


# Esperar y ingresar el código de seguridad
securityCode_field = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.NAME, 'verificationCode')))
securityCode_field[0].send_keys(SECURITYCODE)
time.sleep(1)

# Hacer clic en el botón de inicio de sesión después de la autenticación de dos factores
login2AF_button = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[2]/button')))
login2AF_button[0].click()

os.remove(file_path)


