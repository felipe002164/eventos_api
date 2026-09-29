import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from main import app 


client = TestClient(app)

def test_registro_y_login():
    client.post("/auth/registro", json={"email": "test@correo.com", "password": "1234"})
    respuesta = client.post("/auth/login", json={"email": "test@correo.com", "password": "1234"})
    assert respuesta.status_code == 200
    assert "access_token" in respuesta.json()

def test_login_credenciales_incorrectas():
    respuesta = client.post("/auth/login", json={"email": "noexiste@correo.com", "password": "x"})
    assert respuesta.status_code == 401


def test_crear_evento_require_autenticacion():
    respuesta = client.post("/eventos", json={"nombre": "Charla Pyton", "fecha": "2026-09-01T10:00:00"})
    assert respuesta.status_code == 401 #sin token, debe rechazar