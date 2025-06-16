#rutinas.py
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import Rutina, RutinaEjercicio, Ejercicio, RutinaSerie, Sesion, SesionEjercicio, Usuario
from sqlalchemy.orm import selectinload
from app.schemas import (
    RutinaCreate, RutinaOrdenUpdate, RutinaRead, RutinaSerieRead, RutinaUpdate,
    RutinaEjercicioCreate, RutinaEjercicioRead, RutinaEjercicioUpdate
)
from app.dependencies import get_current_user, get_session

router = APIRouter(tags=["Rutina"])

@router.post("/rutinas", response_model=RutinaRead)
def crear_rutina(
    rutina: RutinaCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    nueva_rutina = Rutina(**rutina.dict(), usuario_id=current_user.id)
    session.add(nueva_rutina)
    session.commit()
    session.refresh(nueva_rutina)
    return nueva_rutina

@router.get("/rutinas", response_model=List[RutinaRead])
def listar_rutinas(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutinas = session.exec(
        select(Rutina).where(
            (Rutina.es_defecto == True) | (Rutina.usuario_id == current_user.id)
        )
    ).all()
    return rutinas

@router.get("/rutinas/{id}", response_model=RutinaRead)
def obtener_rutina(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    if not rutina.es_defecto and rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta rutina")
    return rutina

@router.put("/rutinas/{id}", response_model=RutinaRead)
def actualizar_rutina(
    id: int,
    datos: RutinaUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    if rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta rutina")
    for clave, valor in datos.dict(exclude_unset=True).items():
        setattr(rutina, clave, valor)
    session.add(rutina)
    session.commit()
    session.refresh(rutina)
    return rutina

@router.delete("/rutinas/{id}", status_code=204)
def eliminar_rutina(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    if rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta rutina")

    # 1. Eliminar sesiones relacionadas
    sesiones = session.exec(select(Sesion).where(Sesion.rutina_id == id)).all()
    for sesion in sesiones:
        ejercicios_sesion = session.exec(
            select(SesionEjercicio).where(SesionEjercicio.sesion_id == sesion.id)
        ).all()
        for se in ejercicios_sesion:
            session.delete(se)
        session.delete(sesion)

    # 2. Eliminar ejercicios y sus series
    ejercicios = session.exec(
        select(RutinaEjercicio).where(RutinaEjercicio.rutina_id == id)
    ).all()

    for ej in ejercicios:
        series = session.exec(
            select(RutinaSerie).where(RutinaSerie.rutina_ejercicio_id == ej.id)
        ).all()
        for s in series:
            session.delete(s)
        session.delete(ej)

    # 3. Eliminar la rutina
    session.delete(rutina)
    session.commit()

    return {"mensaje": f"Rutina con ID {id} eliminada correctamente"}

@router.post("/rutinas/{id}/copiar", response_model=RutinaRead)
def copiar_rutina(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    if not rutina.es_defecto:
        raise HTTPException(status_code=403, detail="Solo se pueden copiar rutinas públicas")

    # 1. Copiar la rutina base
    copia_rutina = Rutina(
        nombre=rutina.nombre,
        descripcion=rutina.descripcion,
        usuario_id=current_user.id,
        es_defecto=False
    )
    session.add(copia_rutina)
    session.commit()
    session.refresh(copia_rutina)

    # 2. Obtener ejercicios asociados
    ejercicios = session.exec(
        select(RutinaEjercicio).where(RutinaEjercicio.rutina_id == rutina.id)
    ).all()

    for e in ejercicios:
        # 3. Crear copia del ejercicio
        nuevo_ejercicio = RutinaEjercicio(
            rutina_id=copia_rutina.id,
            ejercicio_id=e.ejercicio_id,
            orden=e.orden,
            comentarios=e.comentarios
        )
        session.add(nuevo_ejercicio)
        session.flush()  # Para obtener nuevo_ejercicio.id

        # 4. Copiar las series de este ejercicio
        series = session.exec(
            select(RutinaSerie).where(RutinaSerie.rutina_ejercicio_id == e.id)
        ).all()

        for s in series:
            nueva_serie = RutinaSerie(
                rutina_ejercicio_id=nuevo_ejercicio.id,
                numero=s.numero,
                repeticiones=s.repeticiones,
                peso=s.peso
            )
            session.add(nueva_serie)

    session.commit()
    return copia_rutina


@router.post("/rutinas/{id}/ejercicios", response_model=RutinaEjercicioRead)
def agregar_ejercicio_a_rutina(
    id: int,
    ejercicio_data: RutinaEjercicioCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    if rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta rutina")

    ejercicio = session.get(Ejercicio, ejercicio_data.ejercicio_id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail=f"Ejercicio con ID {ejercicio_data.ejercicio_id} no encontrado")

    datos = ejercicio_data.dict(exclude_unset=True, exclude={"id"})  # 👈 Evita duplicar clave primaria
    nueva_asociacion = RutinaEjercicio(**datos, rutina_id=id)
    session.add(nueva_asociacion)
    session.commit()
    session.refresh(nueva_asociacion)
    return nueva_asociacion

@router.get("/rutinas/{id}/ejercicios", response_model=List[RutinaEjercicioRead])
def listar_ejercicios_de_rutina(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    if not rutina.es_defecto and rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver los ejercicios de esta rutina")

    ejercicios = session.exec(
        select(RutinaEjercicio)
        .where(RutinaEjercicio.rutina_id == id)
        .order_by(RutinaEjercicio.orden)
        .options(selectinload(RutinaEjercicio.ejercicio))  # carga el ejercicio completo
    ).all()
    return ejercicios

@router.put("/rutina-ejercicio/orden", status_code=200)
def actualizar_orden(
    ordenes: List[RutinaOrdenUpdate] = Body(...),
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if not ordenes:
        raise HTTPException(status_code=400, detail="Lista de ordenes vacía")

    ids = [o.id for o in ordenes]
    orden_vals = [o.orden for o in ordenes]

    if len(set(orden_vals)) != len(orden_vals):
        raise HTTPException(status_code=400, detail="Los valores de orden no pueden repetirse")

    if any(o.orden < 1 for o in ordenes):
        raise HTTPException(status_code=400, detail="Todos los valores de orden deben ser mayores o iguales a 1")

    ejercicios_db = session.exec(
        select(RutinaEjercicio).where(RutinaEjercicio.id.in_(ids))
    ).all()

    if len(ejercicios_db) != len(ordenes):
        raise HTTPException(status_code=400, detail="Algunos IDs no existen")

    for ej in ejercicios_db:
        rutina = session.get(Rutina, ej.rutina_id)
        if not rutina or rutina.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta rutina")

    for o in ordenes:
        ej = next((e for e in ejercicios_db if e.id == o.id), None)
        if ej:
            ej.orden = o.orden
            session.add(ej)

    session.commit()
    return {"mensaje": "Orden actualizado correctamente"}

@router.put("/rutina-ejercicio/{id}", response_model=RutinaEjercicioRead)
def editar_ejercicio_de_rutina(
    id: int,
    datos: RutinaEjercicioUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina_ejercicio = session.get(RutinaEjercicio, id)
    if not rutina_ejercicio:
        raise HTTPException(status_code=404, detail="Asociación rutina-ejercicio no encontrada")

    rutina = session.get(Rutina, rutina_ejercicio.rutina_id)
    if not rutina or rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta rutina")

    for clave, valor in datos.dict(exclude_unset=True).items():
        setattr(rutina_ejercicio, clave, valor)

    session.add(rutina_ejercicio)
    session.commit()
    session.refresh(rutina_ejercicio)
    return rutina_ejercicio

@router.delete("/rutina-ejercicio/{id}", status_code=200)
def eliminar_ejercicio_de_rutina(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina_ejercicio = session.get(RutinaEjercicio, id)
    if not rutina_ejercicio:
        raise HTTPException(status_code=404, detail="Asociación rutina-ejercicio no encontrada")

    rutina = session.get(Rutina, rutina_ejercicio.rutina_id)
    if not rutina or rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta rutina")

    session.delete(rutina_ejercicio)
    session.commit()
    return {"mensaje": f"Asociación con ID {id} eliminada correctamente"}

@router.get("/rutina-ejercicio/{id}/series", response_model=List[RutinaSerieRead])
def listar_series_de_rutina_ejercicio(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(RutinaEjercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    rutina = session.get(Rutina, ejercicio.rutina_id)

    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    if not rutina.es_defecto and rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver estas series")

    return ejercicio.series_detalle

