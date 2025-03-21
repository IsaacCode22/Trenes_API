"# Aplicación de Estación de Trenes - API"


Este proyecto es una API para gestionar estaciones de trenes. Está desarrollado con **FastAPI** y utiliza **MySQL** como base de datos. Además, se conecta con un frontend hecho en **Flet**.


📌**Tecnologías utilizadas**  
```md
## Tecnologías
- Python 3.10
- FastAPI
- MySQL
- Flet



## Características principales
- Gestión de operadores (Creación, edición y asignación de roles).
- Administración de estaciones y trenes.
- Autenticación JWT para seguridad.
- API documentada con Swagger y ReDoc.

---

## Tecnologías utilizadas
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Base de datos:** MySQL
- **Autenticación:** JWT (JSON Web Token)
- **Frontend:** Flet (Python)
- **ORM:** SQLAlchemy
- **Servidor local:** Uvicorn

---

# Crear y activar el entorno virtual
# En Windows
Creacion: python -m venv venv
activacion: venv\Scripts\activate

# En Linux/Mac
Creacion: python3 -m venv venv
Activacion: source venv/bin/activate

#Instalar Dependencias con el siguiente comando:

pip install -r requirements.txt

#Puedes importar la base de datos con: 

mysql -u root -p trenes_db < bd/trenes_db.sql

#Para ejecutar el servidor de la API, utiliza el siguiente comando:

uvicorn Backend.api:app --reload


