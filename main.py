from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime 

from db import get_db, crear_tablas
from modelos import Usuario, Evento, Inscripcion
from esquemas import UsuarioCrear, UsuarioLogin, EventoCrear, EventoRespuesta
from auth import hashear_password, verificar_password, crear_token, obtener_usuario_actual

from fastapi.responses import FileResponse
from fpdf import FPDF
import os 

app = FastAPI()
crear_tablas()

@app.post("/auth/registro", status_code=201)
def registro(datos: UsuarioCrear, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter_by(email=datos.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")

    usuario = Usuario(email=datos.email, hash_password=hashear_password(datos.password))
    db.add(usuario)
    db.commit()
    return {"mensaje": "Usuario registrado con exito"}

@app.post("/auth/login")
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(email=datos.email).first()
    if usuario is None or not verificar_password(datos.password, usuario.hash_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrecta")


    token = crear_token(usuario.id)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/eventos", response_model=EventoRespuesta, status_code=201)
def crear_evento(datos: EventoCrear, db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    evento = Evento(nombre=datos.nombre, fecha=datos.fecha, organizador_id=usuario.id)
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

@app.get("/eventos", response_model=list[EventoRespuesta])
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).all()

@app.post("/eventos/{evento_id}/inscripcion", status_code=201)
def inscribirse(evento_id: int, db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    evento = db.query(Evento).filter_by(id=evento_id).first()
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    ya_inscrito = db.query(Inscripcion).filter_by(evento_id=evento_id, usuario_id=usuario.id).first()
    if ya_inscrito:
        raise HTTPException(status_code=400, detail="Ya estas inscrito en este evento")

    inscripcion = Inscripcion (evento_id=evento_id, usuario_id=usuario.id)
    db.add(inscripcion)
    db.commit()
    return {"mensaje": "Inscripcion exitosa"}

@app.post("/eventos/{evento_id}/confirmar-asistencia")
def confirmar_asistencia(evento_id: int, db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    inscripcion = db.query(Inscripcion).filter_by(evento_id=evento_id, usuario_id=usuario.id).first()
    if inscripcion is None:
        raise HTTPException(status_code=404, detail="No estas inscrito en este evento")

    inscripcion.asistio = True
    db.commit()

    evento = db.query(Evento).filter_by(id=evento_id).first()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=20)
    pdf.cell(0, 40, "Certificado de Asistencia", ln=True, align="C")
    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 20, f"Otorgado a: {usuario.email}", ln=True, align="C")
    pdf.cell(0, 20, f"por asistir a: {evento.nombre}", ln=True, align="C")

    os.makedirs("certificados", exist_ok=True)
    ruta = f"certificados/certificado_{usuario.id}_{evento_id}.pdf"
    pdf.output(ruta)

    return FileResponse(ruta, media_type="application/pdf", filename="certificado.pdf")