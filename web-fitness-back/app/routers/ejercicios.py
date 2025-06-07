from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import Ejercicio, Usuario
from app.schemas import EjercicioCreate, EjercicioRead, EjercicioUpdate
from app.dependencies import get_current_user, get_session

router = APIRouter(tags=["Ejercicio"])

@router.post("/ejercicios", response_model=EjercicioRead)
def crear_ejercicio(
    ejercicio: EjercicioCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    # Si no es admin, ignorar imagen_url y video_url
    data = ejercicio.dict()
    if not current_user.is_admin:
        data["imagen_url"] = None
        data["video_url"] = None

    nuevo_ejercicio = Ejercicio(**data, usuario_id=current_user.id)
    session.add(nuevo_ejercicio)
    session.commit()
    session.refresh(nuevo_ejercicio)
    return nuevo_ejercicio

@router.get("/ejercicios", response_model=List[EjercicioRead])
def listar_ejercicios(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    # Devuelve ejercicios públicos (usuario_id=None) y los creados por el usuario
    ejercicios = session.exec(
        select(Ejercicio).where(
            (Ejercicio.usuario_id == None) | (Ejercicio.usuario_id == current_user.id)
        )
    ).all()
    return ejercicios

@router.get("/ejercicios/{id}", response_model=EjercicioRead)
def obtener_ejercicio(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(Ejercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    # Verificar permisos
    if not current_user.is_admin and ejercicio.usuario_id not in {None, current_user.id}:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este ejercicio")

    return ejercicio

@router.put("/ejercicios/{id}", response_model=EjercicioRead)
def actualizar_ejercicio(
    id: int,
    datos: EjercicioUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(Ejercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    # Verificar permisos
    if not current_user.is_admin and ejercicio.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este ejercicio")

    for clave, valor in datos.dict(exclude_unset=True).items():
        setattr(ejercicio, clave, valor)

    session.add(ejercicio)
    session.commit()
    session.refresh(ejercicio)
    return ejercicio

@router.delete("/ejercicios/{id}", status_code=204)
def eliminar_ejercicio(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(Ejercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    # Verificar permisos
    if not current_user.is_admin and ejercicio.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este ejercicio")

    # No se pueden borrar ejercicios públicos
    if ejercicio.usuario_id is None:
        raise HTTPException(status_code=403, detail="No se pueden eliminar ejercicios públicos")

    session.delete(ejercicio)
    session.commit()
    return {"mensaje": f"Ejercicio con ID {id} eliminado correctamente"}

