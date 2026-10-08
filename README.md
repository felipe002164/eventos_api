Eventos API

API REST para gestionar eventos: los usuarios se registran, inician sesión, se inscriben a eventos y, al confirmar su asistencia, reciben un certificado en PDF. Está desplegada en producción y documentada con Swagger.

Demo en vivo: https://eventosapi-production-4633.up.railway.app/docs

La base de datos usa el plan gratuito de Supabase, que se pausa tras varios días sin actividad. Si la demo no responde, puede ser por eso.

Características
Registro de usuarios con contraseñas cifradas (bcrypt).
Inicio de sesión con JWT y expiración del token.
Creación y listado de eventos.
Inscripción a eventos, con control de inscripciones duplicadas.
Confirmación de asistencia y generación de certificado en PDF.
Rutas protegidas: crear eventos, inscribirse y confirmar asistencia requieren token.
Validación de datos con Pydantic y documentación automática con Swagger.
Tests automatizados con pytest.
Contenedores con Docker y despliegue en la nube.
Tecnologías
Python y FastAPI
SQLAlchemy y PostgreSQL
JWT (python-jose) y passlib con bcrypt
fpdf2 para los certificados
Docker y Docker Compose
pytest
Railway (API) y Supabase (base de datos)
Endpoints
Método	Ruta	Autenticación	Descripción
POST	/auth/registro	No	Crea un usuario
POST	/auth/login	No	Devuelve el token de acceso
GET	/eventos	No	Lista los eventos
POST	/eventos	Sí	Crea un evento
POST	/eventos/{evento_id}/inscripcion	Sí	Inscribe al usuario autenticado
POST	/eventos/{evento_id}/confirmar-asistencia	Sí	Marca la asistencia y devuelve el certificado en PDF
Ejemplo de flujo
Registro: POST /auth/registro
json
{ "email": "usuario@correo.com", "password": "una_clave_segura" }
Login: POST /auth/login con el mismo cuerpo. Responde:
json
{ "access_token": "eyJ...", "token_type": "bearer" }
En las rutas protegidas, envía el header Authorization: Bearer <access_token>.

El botón Authorize de Swagger no sirve para este login, porque /auth/login recibe JSON y ese botón envía el formato de formulario de OAuth2. Para probar las rutas protegidas usa un cliente HTTP como Thunder Client, Postman o curl.

Modelo de datos
Tabla	Campos principales
usuarios	id, email (único), hash_password, es_organizador
eventos	id, nombre, fecha, organizador_id
inscripciones	id, evento_id, usuario_id, asistio, fecha_inscripcion
Estructura del proyecto
eventos-api/
├── main.py             # Endpoints
├── auth.py             # Hash de contraseñas, JWT y usuario actual
├── db.py               # Conexión y sesión de base de datos
├── modelos.py          # Modelos SQLAlchemy
├── esquemas.py         # Esquemas Pydantic
├── tests/
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
Ejecución local

Requisitos: Python 3, Git y Docker Desktop.

powershell
git clone https://github.com/felipe002164/eventos-api.git
cd eventos-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Opción A: base de datos en un contenedor y API con uvicorn
powershell
docker run --name eventos-db -e POSTGRES_PASSWORD=<tu_contraseña> -e POSTGRES_DB=eventos -p 5434:5432 --restart unless-stopped -d postgres
$env:DATABASE_URL = "postgresql://postgres:<tu_contraseña>@localhost:5434/eventos"
uvicorn main:app --reload
Opción B: todo con Docker Compose
powershell
docker-compose up --build

La API queda en http://localhost:8000/docs.

Variables de entorno
Variable	Descripción
DATABASE_URL	Cadena de conexión a PostgreSQL
Tests
powershell
pytest -v

Los tests cubren el registro y login, el rechazo de credenciales incorrectas y la protección de la creación de eventos sin token.

Despliegue
Base de datos: proyecto de Supabase, conectado mediante su connection pooler.
API: servicio de Railway conectado a este repositorio, con la variable DATABASE_URL configurada y el comando de inicio uvicorn main:app --host 0.0.0.0 --port 8000.
Mejoras pendientes
Mover SECRET_KEY a una variable de entorno.
Aplicar el rol de organizador en la creación de eventos.
Guardar los certificados en un almacenamiento externo, porque el disco de Railway no es persistente.
Agregar tests para inscripción y certificados.
Crear una interfaz web que consuma esta API.
