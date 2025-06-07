#progresos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.dependencies import get_current_user
from app.models import Progreso
from app.schemas import ProgresoCreate, ProgresoRead, ProgresoUpdate
from typing import List

router = APIRouter(prefix="/progresos", tags=["Progreso"])

# Crear nuevo progreso
@router.post("", response_model=ProgresoRead)
def crear_progreso(
    data: ProgresoCreate,
    session: Session = Depends(get_session),
    usuario=Depends(get_current_user)
):
    # Verificamos si ya existe un progreso en esa fecha para ese usuario
    existe = session.exec(
        select(Progreso).where(Progreso.usuario_id == usuario.id, Progreso.fecha == data.fecha)
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un progreso en esa fecha")

    progreso = Progreso(**data.dict(), usuario_id=usuario.id)
    session.add(progreso)
    session.commit()
    session.refresh(progreso)
    return progreso

# Listar todos los progresos del usuario
@router.get("", response_model=List[ProgresoRead])
def listar_progresos(
    session: Session = Depends(get_session),
    usuario=Depends(get_current_user)
):
    return session.exec(
        select(Progreso).where(Progreso.usuario_id == usuario.id).order_by(Progreso.fecha.desc())
    ).all()

# Obtener un progreso concreto
@router.get("/{progreso_id}", response_model=ProgresoRead)
def obtener_progreso(
    progreso_id: int,
    session: Session = Depends(get_session),
    usuario=Depends(get_current_user)
):
    progreso = session.get(Progreso, progreso_id)
    if not progreso or progreso.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso

# Editar peso o comentarios
@router.put("/{progreso_id}", response_model=ProgresoRead)
def actualizar_progreso(
    progreso_id: int,
    data: ProgresoUpdate,
    session: Session = Depends(get_session),
    usuario=Depends(get_current_user)
):
    progreso = session.get(Progreso, progreso_id)
    if not progreso or progreso.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(progreso, k, v)

    session.commit()
    session.refresh(progreso)
    return progreso

# Eliminar un progreso
@router.delete("/{progreso_id}", status_code=204)
def eliminar_progreso(
    progreso_id: int,
    session: Session = Depends(get_session),
    usuario=Depends(get_current_user)
):
    progreso = session.get(Progreso, progreso_id)
    if not progreso or progreso.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")

    session.delete(progreso)
    session.commit()
