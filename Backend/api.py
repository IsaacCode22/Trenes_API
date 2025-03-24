from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, List
import jwt
from datetime import datetime, timedelta, timezone
import mysql.connector
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKeyHeader
from Backend.seguridad import hash_password, verify_password
from fastapi.responses import JSONResponse

api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

SECRET_KEY = "holamundo"  # Cambia por una clave segura

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API de Trenes",
        version="1.0.0",
        description="API para gestionar estaciones de trenes con autenticación JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

# Modelos de datos
class Estacion(BaseModel):
    id: Optional[int] = None
    operador: str
    contrasena: str
    nombre: str
    horarios: List[str]
    precio: float
    estado: str
    boletos_vendidos: int

class Tren(BaseModel):
    id: Optional[int] = None
    nombre: str

class TrenEstacion(BaseModel):
    id: Optional[int] = None
    tren_id: int
    estacion_id: int
    hora_aproximada: str

# Función para obtener la conexión a MySQL
def get_db():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="trenes_db"
    )
    try:
        yield db
    finally:
        db.close()

# Verificación de token JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
# Modelo de datos para el inicio de sesión
class LoginRequest(BaseModel):
    operador: str
    contrasena: str

# Endpoint de inicio de sesión
@app.post("/login")
def login():
    return 0


@app.get("/saludo/")
def saludo():
        return {"mensaje": "Bienvenidos a la API de trenes"}

# Endpoints de estaciones

@app.get("/estaciones/{estacion_id}", response_model=Estacion)
def get_estacion_por_id(estacion_id: int, payload: dict = Depends(verify_token), db: mysql.connector = Depends(get_db)):
    cursor = db.cursor()
    
    if payload["rol"] == "operador" and payload["id"] != estacion_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta estación")

    cursor.execute("SELECT * FROM estaciones WHERE id = %s", (estacion_id,))
    result = cursor.fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    return Estacion(
        id=result[0], operador=result[1], contrasena=result[2], nombre=result[3], 
        horarios=result[4].split(", "), precio=result[5], estado=result[6], boletos_vendidos=result[7]
    )



@app.get("/estaciones", response_model=List[Estacion])
def get_estaciones(payload: dict = Depends(verify_token), db: mysql.connector = Depends(get_db)):
    cursor = db.cursor()
    if payload["rol"] == "admin":
        cursor.execute("SELECT * FROM estaciones")
    else:
        cursor.execute("SELECT * FROM estaciones WHERE id = %s", (payload["id"],))
    results = cursor.fetchall()

    print("Resultados de la BD:", results)  # 📌 Depuración
    
    estaciones = [
        Estacion(
            id=row[0], operador=row[1], contrasena=row[2], nombre=row[3], 
            horarios=row[4].split(", "),  # Convertir de string a lista
            precio=row[5], estado=row[6], boletos_vendidos=row[7]
        )
        for row in results
    ]

    print("Estaciones enviadas al frontend:", estaciones)  # 📌 Depuración
    return estaciones


@app.post("/estaciones", response_model=Estacion, status_code=201)
def create_estacion(estacion: Estacion, payload: dict = Depends(verify_token), db: mysql.connector = Depends(get_db)):
    if payload["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")

    cursor = db.cursor()

    # Verificar si el operador ya existe en la base de datos
    cursor.execute("SELECT id FROM estaciones WHERE operador = %s", (estacion.operador,))
    existe = cursor.fetchone()
    
    if existe:
        raise HTTPException(status_code=400, detail="El operador ya existe")

    # Convertir la lista de horarios en un string separado por comas
    horarios_str = ", ".join(estacion.horarios)

    hashed_password = hash_password(estacion.contrasena)

    try:
        cursor.execute(
            "INSERT INTO estaciones (operador, contrasena, nombre, horarios, precio, estado, boletos_vendidos) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (estacion.operador, hashed_password, estacion.nombre, horarios_str, 
             estacion.precio, estacion.estado, estacion.boletos_vendidos)
        )
        db.commit()  # Guardar los cambios
        id_generado = cursor.lastrowid  # Obtener el ID generado
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Código de error para entrada duplicada en MySQL
            raise HTTPException(status_code=400, detail="El operador ya existe en la base de datos")
        else:
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")

    return Estacion(
        id=id_generado,
        operador=estacion.operador,
        contrasena=hashed_password,
        nombre=estacion.nombre,
        horarios=estacion.horarios,
        precio=estacion.precio,
        estado=estacion.estado,
        boletos_vendidos=estacion.boletos_vendidos
    )

@app.delete("/estaciones/{estacion_id}")
def delete_estacion(estacion_id: int, payload: dict = Depends(verify_token), db: mysql.connector = Depends(get_db)):
    if payload["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar estaciones")

    cursor = db.cursor()

    # Verificar si la estación existe antes de eliminarla
    cursor.execute("SELECT * FROM estaciones WHERE id = %s", (estacion_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Estación no encontrada")

    # Eliminar la estación
    cursor.execute("DELETE FROM estaciones WHERE id = %s", (estacion_id,))
    db.commit()

    return {"message": f"Estación con ID {estacion_id} eliminada exitosamente"}


# Endpoints de trenes
@app.get("/trenes", response_model=List[Tren])
def get_trenes(db: mysql.connector = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM trenes")
    results = cursor.fetchall()
    return [Tren(id=row[0], nombre=row[1]) for row in results]

# Endpoints de trenes-estaciones
@app.get("/trenes-estaciones", response_model=List[TrenEstacion])
def get_trenes_estaciones(estacion_id: Optional[int] = None, tren_id: Optional[int] = None, db: mysql.connector = Depends(get_db)):
    cursor = db.cursor()
    if estacion_id:
        cursor.execute("SELECT * FROM trenes_estaciones WHERE estacion_id = %s", (estacion_id,))
    elif tren_id:
        cursor.execute("SELECT * FROM trenes_estaciones WHERE tren_id = %s", (tren_id,))
    else:
        cursor.execute("SELECT * FROM trenes_estaciones")
    results = cursor.fetchall()
    return [TrenEstacion(id=row[0], tren_id=row[1], estacion_id=row[2], hora_aproximada=row[3]) for row in results]

#verifica la conexion a la base de datos
@app.get("/status")
def check_db_status(db: mysql.connector = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT 1")  # Ejecuta una consulta simple
        return {"status": "Conectado a la base de datos"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
