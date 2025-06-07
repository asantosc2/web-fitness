from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import date
from app.models import Sesion, Rutina, RutinaEjercicio, SesionEjercicio, Usuario
from app.schemas import SesionCreate, SesionEjercicioCreate, SesionEjercicioUpdate, SesionRead, SesionEjercicioRead
from app.dependencies import get_current_user, get_session

router = APIRouter(tags=["Sesion"])

@router.post("/sesiones", response_model=SesionRead)
def crear_sesion(
    sesion_data: SesionCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    nueva_sesion = Sesion(
        usuario_id=current_user.id,
        fecha=date.today(),
        rutina_id=sesion_data.rutina_id,
        nota=sesion_data.nota
    )
    session.add(nueva_sesion)
    session.commit()
    session.refresh(nueva_sesion)

    if sesion_data.rutina_id:
        ejercicios = session.exec(
            select(RutinaEjercicio).where(RutinaEjercicio.rutina_id == sesion_data.rutina_id)
        ).all()

        for e in ejercicios:
            copia = SesionEjercicio(
                sesion_id=nueva_sesion.id,
                ejercicio_id=e.ejercicio_id,
                orden=e.orden,
                series=e.series,
                repeticiones=e.repeticiones,
                peso=0.0,
                comentarios=e.comentarios
            )
            session.add(copia)

    session.commit()
    return nueva_sesion

# 🔹 Añadir ejercicios manualmente a una sesión
@router.post("/sesiones/{id}/ejercicios", response_model=List[SesionEjercicioRead])
def agregar_ejercicios_a_sesion(
    id: int,
    ejercicios: List[SesionEjercicioCreate],
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    sesion = session.get(Sesion, id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta sesión")

    nuevos = []
    for data in ejercicios:
        nuevo = SesionEjercicio(**data.dict(), sesion_id=id)
        session.add(nuevo)
        nuevos.append(nuevo)

    session.commit()
    for ej in nuevos:
        session.refresh(ej)
    return nuevos

# 🔹 Ver ejercicios de una sesión
@router.get("/sesiones/{id}/ejercicios", response_model=List[SesionEjercicioRead])
def listar_ejercicios_de_sesion(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    sesion = session.get(Sesion, id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta sesión")

    ejercicios = session.exec(
        select(SesionEjercicio).where(SesionEjercicio.sesion_id == id).order_by(SesionEjercicio.orden)
    ).all()
    return ejercicios

# 🔹 Editar un ejercicio
@router.put("/sesion-ejercicio/{id}", response_model=SesionEjercicioRead)
def actualizar_ejercicio_sesion(
    id: int,
    datos: SesionEjercicioUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(SesionEjercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    sesion = session.get(Sesion, ejercicio.sesion_id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta sesión")

    for clave, valor in datos.dict(exclude_unset=True).items():
        setattr(ejercicio, clave, valor)

    session.add(ejercicio)
    session.commit()
    session.refresh(ejercicio)
    return ejercicio

# 🔹 Eliminar un ejercicio
@router.delete("/sesion-ejercicio/{id}", status_code=204)
def eliminar_ejercicio_sesion(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(SesionEjercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    sesion = session.get(Sesion, ejercicio.sesion_id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este ejercicio")

    session.delete(ejercicio)
    session.commit()
    return {"mensaje": f"Ejercicio con ID {id} eliminado correctamente"}
