from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime 


Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    es_organizador = Column(Boolean, default=False)

class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    fecha = Column(DateTime, nullable=False)
    organizador_id = Column(Integer, ForeignKey("usuarios.id"))


class Inscripcion(Base):
    __tablename__ = "inscripciones"
    id = Column(Integer, primary_key=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    asistio = Column(Boolean, default=False)
    fecha_inscripcion = Column(DateTime, default=datetime.utcnow)