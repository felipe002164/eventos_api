from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioCrear(BaseModel):
    email : EmailStr
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class EventoCrear(BaseModel):
    nombre: str
    fecha: datetime

class EventoRespuesta(EventoCrear):
    id: int
    class Config:
        from_attributes = True