import mysql.connector
from seguridad import hash_password, verify_password  # Importa tus funciones de seguridad

# Conexión a la base de datos
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="trenes_db"
)
cursor = db.cursor()

def encriptar_contraseñas():
    """Encripta solo las contraseñas que aún no están encriptadas."""
    cursor.execute("SELECT id, contrasena FROM estaciones")
    usuarios = cursor.fetchall()

    for id_usuario, contraseña_actual in usuarios:
        if contraseña_actual.startswith("$2b$"):  # Verifica si ya está encriptada
            print(f"⚠️ Usuario {id_usuario} ya tiene una contraseña encriptada, se omite.")
            continue

        contraseña_encriptada = hash_password(contraseña_actual)
        cursor.execute("UPDATE estaciones SET contrasena = %s WHERE id = %s", (contraseña_encriptada, id_usuario))

    db.commit()
    print("✅ Encriptación completada.")


def verificar_contraseña():
    """Verifica si una contraseña ingresada coincide con la almacenada en la base de datos."""
    operador_input = input("Ingrese el nombre del operador: ")
    contrasena_input = input("Ingrese la contraseña a verificar: ")

    cursor.execute("SELECT contrasena FROM estaciones WHERE operador = %s", (operador_input,))
    resultado = cursor.fetchone()

    if resultado:
        contraseña_encriptada = resultado[0]
        if verify_password(contrasena_input, contraseña_encriptada):
            print("✅ La contraseña es válida.")
        else:
            print("❌ La contraseña es incorrecta.")
    else:
        print("⚠️ El operador no existe.")

# Menú para seleccionar la opción deseada
print(" Seleccione una opción:")
print("1 - Encriptar todas las contraseñas")
print("2 - Verificar una contraseña")
opcion = input("Ingrese el número de opción: ")

if opcion == "1":
    encriptar_contraseñas()
elif opcion == "2":
    verificar_contraseña()
else:
    print("⚠️ Opción no válida.")

# Cerrar la conexión
cursor.close()
db.close()
