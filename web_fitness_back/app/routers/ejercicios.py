from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import Ejercicio, Usuario, EjercicioFoto
from app.schemas import EjercicioCreate, EjercicioRead, EjercicioUpdate
from app.dependencies import get_current_user, get_session
from sqlalchemy.orm import selectinload

router = APIRouter(tags=["Ejercicio"])

@router.post("/ejercicios", response_model=EjercicioRead)
def crear_ejercicio(
    ejercicio: EjercicioCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    data = ejercicio.dict(exclude={"fotos"})
    if not current_user.is_admin:
        data["video_url"] = None

    nuevo = Ejercicio(**data, usuario_id=current_user.id)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)

    # Añadir fotos si las hay
    for url in ejercicio.fotos or []:
        foto = EjercicioFoto(url=url, ejercicio_id=nuevo.id)
        session.add(foto)

    session.commit()
    session.refresh(nuevo)
    return nuevo


@router.get("/ejercicios", response_model=List[EjercicioRead])
def listar_ejercicios(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    # Devuelve ejercicios públicos (usuario_id=None) y los creados por el usuario
    ejercicios = session.exec(
        select(Ejercicio)
        .options(selectinload(Ejercicio.fotos))
        .where((Ejercicio.usuario_id == None) | (Ejercicio.usuario_id == current_user.id))
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

    if not current_user.is_admin and ejercicio.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este ejercicio")

    # Excluir fotos de los datos actualizables
    for clave, valor in datos.dict(exclude_unset=True, exclude={"fotos"}).items():
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

