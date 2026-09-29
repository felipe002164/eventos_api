from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import get_db
from modelos import Usuario

SECRET_KEY = "clave-secreta-de-desarrollo" # en produccion: variable de entorno 
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password: str, hash_guardado: str)-> bool:
    return pwd_context.verify(password, hash_guardado)

def crear_token(usuario_id: int) -> str:
    payload = {"sub": str(usuario_id), "exp": datetime.utcnow() + timedelta(hours=2)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")

    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario