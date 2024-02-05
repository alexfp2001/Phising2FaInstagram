import json
import mysql.connector

# Función para escapar los caracteres problemáticos
def escape_special_characters(text):
    # Reemplaza los emojis con su representación de escape Unicode
    return text.encode('unicode-escape').decode('utf-8')

# Configuración de la conexión a la base de datos MySQL
config = {
    'user': 'root',
    'password': 'alex',
    'host': '127.0.0.1',
    'database': 'instagram',
    'charset': 'utf8mb4',
    'port': 3306,
}

try:
    # Conectarse a la base de datos
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Mensaje de conexión exitosa
    print("Conexión exitosa a la base de datos MySQL")

    # Define los datos que deseas actualizar
    nombre_usuario = 'pacosoto23'
    lista_contactos = ["Lucas Saeta\n669446811", "Mercedes Coche\n661674362", "Nicoo \ud83d\ude08 Uatd\n639525130"]
    lista_contactos_json = json.dumps([escape_special_characters(contacto) for contacto in lista_contactos])

    # Define la consulta SQL para actualizar el usuario
    sql_query = """
        UPDATE users
        SET 
            lista_contactos = %s
        WHERE name = %s
    """

    # Ejecuta la consulta SQL
    cursor.execute(sql_query, (
        lista_contactos_json,
        nombre_usuario
    ))

    # Confirma los cambios en la base de datos
    conn.commit()
    print("Usuario actualizado exitosamente")

except mysql.connector.Error as error:
    print("Error al conectar a la base de datos MySQL:", error)

finally:
    # Cierra la conexión con la base de datos
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexión a la base de datos MySQL cerrada")
