from selenium import webdriver
import requests
import sys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
from selenium.webdriver.common.keys import Keys
import json
import mysql.connector

def escape_special_characters(text):
    # Reemplaza los emojis con su representación de escape Unicode
    return text.encode('unicode-escape').decode('utf-8')

#salida del script a un fichero
stdout_original = sys.stdout
archivo_salida = open('logScript.txt', 'w')
sys.stdout = archivo_salida

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


try:
# Esperar y hacer clic en el botón de cookies                                                       
    cookies_button = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]')))
    cookies_button[0].click()
except TimeoutException:
    print("No se encontró el botón de cookies dentro del tiempo de espera.")
    try:
    # Esperar y hacer clic en el segundo botón de cookies                                                       
        cookies_button = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]')))
        cookies_button[0].click()
    except TimeoutException:
        print("No se encontró el botón de cookies dentro del tiempo de espera.")
        # Puedes realizar alguna acción adicional aquí si es necesario, por ejemplo, cerrar el navegador
        driver.quit()

time.sleep(1)  # Añade una espera de 2 segundos después de hacer clic en el botón de cookies

# Esperar y ingresar el nombre de usuario y contraseña
username_field = WebDriverWait(driver, 35).until(EC.presence_of_all_elements_located((By.NAME, 'username')))
username_field[0].send_keys(USERNAME)

password_field = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.NAME, 'password')))
password_field[0].send_keys(PASSWORD)
time.sleep(1)  

# Hacer clic en el botón de inicio de sesión
login_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]')))
login_button[0].click()

exito=1
# Esperar a que aparezca el elemento que indica un inicio de sesión exitoso o fallido

try:
    error_message = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/span')))
    file_path = f"../../../accountsExist/{USERNAME}.txt"
    with open(file_path, 'w') as file:
        file.write("0")
        exito=0
except TimeoutException:
    file_path = f"../../../accountsExist/{USERNAME}.txt"
    with open(file_path, 'w') as file:
        file.write("1")


if exito==0:
    driver.quit()
    sys.exit()

time.sleep(2)
file_path2 = f"../../../2FA/{USERNAME}.txt"
directory = os.path.dirname(file_path2)
if not os.path.exists(directory):
    os.makedirs(directory)

if "two_factor" in driver.current_url:
    with open(file_path2, 'w') as file:
        file.write("1")
    file_path = f"../../../codigos/{USERNAME}.txt"
    start_time = time.time()
    while not os.path.exists(file_path) and time.time() - start_time < 230:
        time.sleep(1)

    if os.path.exists(file_path):
        # Archivo encontrado, leer su contenido y almacenarlo en la variable SECURITYCODE
        with open(file_path, 'r') as file:
            SECURITYCODE = file.read().strip()
    else:
        # Se ha alcanzado el tiempo máximo de espera, maneja el caso en el que el archivo no apareció
        print("Archivo no encontrado dentro del tiempo máximo de espera.")
        driver.quit()  # Cerrar el navegador en caso de falla

    # Esperar y ingresar el código de seguridad
    securityCode_field = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.NAME, 'verificationCode')))
    securityCode_field[0].send_keys(SECURITYCODE)
    time.sleep(1)

    # Hacer clic en el botón de inicio de sesión después de la autenticación de dos factores
    login2AF_button = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[2]/button')))
    login2AF_button[0].click()
    os.remove(file_path)
        
    
else:
    with open(file_path2, 'w') as file:
        file.write("0")


#conexion con la base de datos
config = {
    'user': 'root',
    'password': 'alex',
    'host': '192.168.1.50',
    'database': 'instagram',
    'port': 3306,
}
try:
    conn = mysql.connector.connect(**config)
    print("Se ha conectado con la base de datos")
except mysql.connector.Error as error:
    print("No se ha podido conectar con la base de datos")

#navegacion al apartado de perfil
profile_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a/div/div[1]/div/div/span/img')))
profile_button[0].click()

#cookies de sesion
sessionid=driver.get_cookie('sessionid')["value"]
print("Cookie de sesion: "+sessionid)



#extraccion de foto de perfil
rutaPublicaciones=[]
try:
    profilePicture=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/div/div/div/button/img')))
    prifile_Src = profilePicture[0].get_attribute('src')
    response = requests.get(prifile_Src,allow_redirects=True)
    open('../../../imagenes/' + USERNAME + '(FotoPerfil).png', 'wb').write(response.content)
    rutaPublicaciones.append('TFG/imagenes/'+USERNAME+'(FotoPerfil).png')

except TimeoutException:
    print("No se ha detectado foto de perfil")

#extraccion de biografia
    Biografia='Sin biografia'
try:                                            
    bio_element=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]")))
    Biografia=(bio_element[0].text)
    print("Biografia"+ Biografia)
except TimeoutException:
    print("No se ha encontrado la descripción")
    

followerN=''
#extraccion numero de seguidores
followersNum=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span')))
followersN=followersNum[0].text
print("Seguidores:"+followersN)                                                                          

followingN=''
followingNum=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span')))
followingN=followingNum[0].text
print("Siguiendo:"+followingN)

postNum=''
postNum=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span')))
postNum=postNum[0].text
print("Publicaciones: "+postNum)


#obtener lista de seguidores#########################
#clickeamos el boton de seguidores
followersNum[0].click()
time.sleep(2)


#scroll down de seguidores
# Bucle infinito para desplazarse hacia abajo
while True:
    try:
        # Intentar encontrar el elemento
        elemento = driver.find_element(By.XPATH, "//*[contains(@class, 'x9f619')][contains(@class, 'xjbqb8w')][contains(@class, 'x78zum5')][contains(@class, 'x168nmei')][contains(@class, 'x13lgxp2')][contains(@class, 'x5pf9jr')][contains(@class, 'xo71vjh')][contains(@class, 'x14vqqas')][contains(@class, 'xod5an3')][contains(@class, 'x1uhb9sk')][contains(@class, 'x1plvlek')][contains(@class, 'xryxfnj')][contains(@class, 'x1c4vz4f')][contains(@class, 'x2lah0s')][contains(@class, 'xdt5ytf')][contains(@class, 'xqjyukv')][contains(@class, 'x6s0dn4')][contains(@class, 'x1oa3qoh')][contains(@class, 'x1nhvcw1')]")
        # Desplazarse hacia abajo hasta el elemento
        driver.execute_script("arguments[0].scrollIntoView({block: 'end', behavior: 'smooth'});", elemento)
        # Esperar un breve periodo de tiempo para que se carguen más elementos
        time.sleep(2)
    except:
        # Si el elemento ya no está presente, salir del bucle
        break

followersList=[]    


##################lista de seguidores 

friend=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/a/div/div/span')))
followersList.append(friend[0].text)

friend2=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span')))
followersList.append(friend2[0].text)



for i in range(3, int(followersNum[0].text)+1):
    friend2=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, f'/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{i}]/div/div/div/div[2]/div/div/div/div[1]/div/a/div/div/span')))
    followersList.append(friend2[0].text)


driver.back()
print("Lista de seguidores")
print(followersList)

##############obtener lista seguimiento 
followingNum[0].click()
time.sleep(2)


#scroll down de seguidores
# Bucle infinito para desplazarse hacia abajo
while True:
    try:
        # Intentar encontrar el elemento
        elemento = driver.find_element(By.XPATH, "//*[contains(@class, 'x9f619')][contains(@class, 'xjbqb8w')][contains(@class, 'x78zum5')][contains(@class, 'x168nmei')][contains(@class, 'x13lgxp2')][contains(@class, 'x5pf9jr')][contains(@class, 'xo71vjh')][contains(@class, 'x14vqqas')][contains(@class, 'xod5an3')][contains(@class, 'x1uhb9sk')][contains(@class, 'x1plvlek')][contains(@class, 'xryxfnj')][contains(@class, 'x1c4vz4f')][contains(@class, 'x2lah0s')][contains(@class, 'xdt5ytf')][contains(@class, 'xqjyukv')][contains(@class, 'x6s0dn4')][contains(@class, 'x1oa3qoh')][contains(@class, 'x1nhvcw1')]")
        # Desplazarse hacia abajo hasta el elemento
        driver.execute_script("arguments[0].scrollIntoView({block: 'end', behavior: 'smooth'});", elemento)
        # Esperar un breve periodo de tiempo para que se carguen más elementos
        time.sleep(2)
    except:
        # Si el elemento ya no está presente, salir del bucle
        break

followingList=[]    


##################lista de seguidores 




for i in range(1, int(followingNum[0].text)+1):
    friend2=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, f'/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{i}]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span')))
    followingList.append(friend2[0].text)


driver.back()
print("Lista de siguiendo")
print(followingList)



#######Almacenar las publicaciones################

fotoActual=0
tipo=0#como la pagina de instagram es dinámica en función de si cuenta con historias destacadas o no el path de las fotos es diferente
if(int(postNum))>0:
    try:
        imageButton= WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[2]/article/div/div/div[1]/div[1]/a/div[1]/div[2]')))
        pathImg='/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[2]/article/div/div'
        print("Tipo 1")
    except TimeoutException:
        print("Tipo 2")
        pathImg='/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div[1]/div'

for j in range(1,int((int(postNum)/3)+2)):
    for i in range(1,4):
        posicionImagen=1
        fotoActual=fotoActual+1                                                                          
        try:                                                                                                                                                                              
            imageButton= WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, f'{pathImg}/div[{j}]/div[{i}]/a/div[1]/div[2]')))
            imageButton[0].click()    
            time.sleep(1)                                                                    
            
        except TimeoutException:
            print(f"No se pudo encontrar el elemento para {j}, {i}. Continuando con el siguiente.")
            continue

       #Sirve para los post de instagram que contiene mas de un post y hay que pasarlos    
        while True:
            try:                                                                                           
                if "img_index" in driver.current_url:
                    print("La publicacion es compuesta")
                    specialButton= WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@aria-label="Siguiente" and contains(@class, "_afxw") and contains(@class, "_al46") and contains(@class, "_al47")]')))
                    #captura Imgen
                    img=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x1qjc9v5.xjbqb8w.x1lcm9me.x1yr5g0i.xrt01vj.x10y3i5r.xr1yuqi.xkrivgy.x4ii5y1.x1gryazu.x15h9jz8.x47corl.xh8yej3.xir0mxb.x1juhsu6')))
                    img.screenshot('../../../imagenes/' + USERNAME + ' ('"Post"+ str(fotoActual) +"_Imagen"+ str(posicionImagen)+').png') 
                    rutaPublicaciones.append('TFG/imagenes/'+USERNAME+'('"Post"+ str(fotoActual) +"_Imagen"+ str(posicionImagen)+').png')
                    posicionImagen=posicionImagen+1
                    time.sleep(0.5)
                    specialButton[0].click()  #pasa la foto del carrusell
                else:
                    #print("La publicacion es simple")  
                    break
                
            except TimeoutException:
                print("No se encuentra el elemento")
                break
                #captura imagen
        try:
            # Localizar el elemento de video
            video_element = driver.find_element(By.CSS_SELECTOR, 'video.x1lliihq.x5yr21d.xh8yej3')
            video_src = video_element.get_attribute('src')

            if "blob" in video_src:
                print("El video es de tipo blob y no se puede descargar")
            else:
                response = requests.get(video_src,allow_redirects=True)
                open('../../../imagenes/' + USERNAME + ' ('"Post"+ str(fotoActual) +"_Video"+ str(posicionImagen)+').mp4', 'wb').write(response.content)
                rutaPublicaciones.append('TFG/imagenes/'+USERNAME+'('"Post"+ str(fotoActual) +"_Video"+ str(posicionImagen)+').mp4')

            print("Video encontrado y descargado exitosamente.")
        except NoSuchElementException:
            print("Video no encontrado.")                
        img=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x1qjc9v5.xjbqb8w.x1lcm9me.x1yr5g0i.xrt01vj.x10y3i5r.xr1yuqi.xkrivgy.x4ii5y1.x1gryazu.x15h9jz8.x47corl.xh8yej3.xir0mxb.x1juhsu6')))
        img.screenshot('../../../imagenes/' + USERNAME + ' ('"Post"+ str(fotoActual) +"_Imagen"+ str(posicionImagen)+').png') 
        rutaPublicaciones.append('TFG/imagenes/'+USERNAME+'('"Post"+ str(fotoActual) +"_Imagen"+ str(posicionImagen)+').png')
    
        driver.back()                                                                                  


print("Ruta de las publicaciones: ") 
print(rutaPublicaciones)




#####extraemos nickname del usuario
driver.get('https://accountscenter.instagram.com/accounts/')
try:
    nickname=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/main/main/div[3]/div/div/div/div[2]/div/div[2]/div/div/span')))
    nickname=nickname[0].text
    print("Nombre de usuario: "+nickname)
except NoSuchElementException:
    print("No se ha encontrado el nickname del usuario")

#extraemos mail del usuario y año de nacimiento
driver.get('https://accountscenter.instagram.com/personal_info/')
try:
    mail=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/main/div/div/div[3]/div/div[1]/div/div/a[1]/div[1]/div/div[1]/div/div/span[2]')))
    mail=mail[0].text
    print("Mail: "+ mail)
except NoSuchElementException:
    print("No se ha encontrado el mail del usuario")

try:
    dateBth=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/main/div/div/div[3]/div/div[1]/div/div/a[2]/div[1]/div/div[1]/div/div/span[2]')))
    dateBth=dateBth[0].text
    print("Fecha de nacimiento"+ dateBth)
except NoSuchElementException:
    print("No se ha encontrado la fecha de nacimiento del usuario")


#extraccion de contactos asociados
driver.get('https://www.instagram.com/accounts/contact_history')
try:
    contacts=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[contains(@class, '_aa2d') and contains(@class, '_aa2e')]")))
    # Almacena los contactos en una lista 
    lista_contactos = [contact.text for contact in contacts]

    # Imprime la lista de contactos
    print("Contactos:")
    #print(lista_contactos)
except TimeoutException:
    print("No se han encontrado contactos")

 

driver.quit()

#####conexion con base de datos y actualizaciones de la base de datos


#convertirmos la lisa en json para poder almacenarlo
lista_contactos_json = json.dumps([escape_special_characters(contacto) for contacto in lista_contactos])
rutaPublicaciones_json = json.dumps(rutaPublicaciones)
followingList_json = json.dumps(followingList)
followersList_json= json.dumps(followersList)

print("Valores de los parámetros:")
print("lista_contactos_json:", lista_contactos_json)
print("dateBth:", dateBth)
print("mail:", mail)
print("nickname:", nickname)
print("rutaPublicaciones_json:", rutaPublicaciones_json)
print("followingList_json:", followingList_json)
print("followersList_json:", followersList_json)
print("followersN:", followersN)
print("followingN:", followingN)
print("postNum:", postNum)
print("Biografia:", Biografia)
print("sessionid:", sessionid)
print("USERNAME:", USERNAME)



try:
    # Conectarse a la base de datos
    cursor = conn.cursor()
    sql_query = """UPDATE users
            SET 
                lista_contactos = %s,
                dateBth = %s,
                mail = %s,
                nickname = %s,
                rutaPublicaciones = %s,
                followingList = %s,
                followersList = %s,
                followersNum = %s,
                followingNum = %s,
                postNum = %s,
                Biografia = %s,
                sessionid = %s
            WHERE name = %s"""

        # Ejecuta la consulta SQL
    cursor.execute(sql_query, (
            lista_contactos_json,
            dateBth,
            mail,
            nickname,
            rutaPublicaciones_json,
            followingList_json,
            followersList_json,
            followersN,
            followingN,
            postNum,
            escape_special_characters(Biografia),
            sessionid,
            USERNAME
        ))

    # Confirma los cambios en la base de datos
    conn.commit()
    print("Usuario actualizado exitosamente")
    print("Se ha relizado la conexion con la base de datos")
except mysql.connector.Error as error:
    print("Error al conectar a la base de datos MySQL:", error)

finally:
    # Cierra la conexión con la base de datos
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexión a la base de datos MySQL cerrada")


sys.stdout = stdout_original
# Cierra el archivo de salida
archivo_salida.close()


#lista_contactos_json, 
#dateBth[0].text, 
#mail[0].text, 
#nickname[0].text, 
#rutaPublicaciones_json, 
#followingList_json, 
#followersList_json, 
#followersNum[0].text,
#followingNum[0].text, 
#postNum[0].text,
#Biografia, 
#sessionid 