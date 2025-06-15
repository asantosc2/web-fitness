from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import Rutina, RutinaEjercicio, Ejercicio, RutinaSerie, SesionEjercicio, Usuario
from sqlalchemy.orm import selectinload
from app.schemas import (
    RutinaCreate, RutinaRead, RutinaSerieRead, RutinaUpdate,
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

    # 1. Copiar la rutina
    copia_rutina = Rutina(
        nombre=rutina.nombre,
        descripcion=rutina.descripcion,
        usuario_id=current_user.id,
        es_defecto=False
    )
    session.add(copia_rutina)
    session.commit()
    session.refresh(copia_rutina)

    # 2. Copiar los ejercicios asociados
    ejercicios = session.exec(
        select(RutinaEjercicio).where(RutinaEjercicio.rutina_id == rutina.id)
    ).all()

    for ej in ejercicios:
        nuevo_ej = RutinaEjercicio(
            rutina_id=copia_rutina.id,
            ejercicio_id=ej.ejercicio_id,
            orden=ej.orden,
            series=ej.series,
            repeticiones=ej.repeticiones,
            comentarios=ej.comentarios
        )
        session.add(nuevo_ej)
        session.flush()  # importante para obtener nuevo_ej.id

        # 3. Copiar las series de este ejercicio
        series = session.exec(
            select(RutinaSerie).where(RutinaSerie.rutina_ejercicio_id == ej.id)
        ).all()

        for s in series:
            nueva_serie = RutinaSerie(
                rutina_ejercicio_id=nuevo_ej.id,
                numero=s.numero,
                repeticiones=s.repeticiones,
                peso=s.peso
            )
            session.add(nueva_serie)

    session.commit()
    return copia_rutina


@router.post("/rutinas/{id}/ejercicios", response_model=List[RutinaEjercicioRead])
def agregar_ejercicios_a_rutina(
    id: int,
    ejercicios: List[RutinaEjercicioCreate],
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    if rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta rutina")

    nuevas_asociaciones = []
    for ejercicio_data in ejercicios:
        ejercicio = session.get(Ejercicio, ejercicio_data.ejercicio_id)
        if not ejercicio:
            raise HTTPException(status_code=404, detail=f"Ejercicio con ID {ejercicio_data.ejercicio_id} no encontrado")
        nueva_asociacion = RutinaEjercicio(**ejercicio_data.dict(), rutina_id=id)
        session.add(nueva_asociacion)
        nuevas_asociaciones.append(nueva_asociacion)

    session.commit()
    for asociacion in nuevas_asociaciones:
        session.refresh(asociacion)
    return nuevas_asociaciones

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

@router.delete("/rutina-ejercicio/{id}", status_code=204)
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

@router.get("/rutinas/{rutina_id}/ejercicios/{rutina_ejercicio_id}/series", response_model=List[RutinaSerieRead])
def listar_series_de_rutina_ejercicio(
    rutina_id: int,
    rutina_ejercicio_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    # Verifica que la rutina sea accesible por el usuario
    rutina = session.get(Rutina, rutina_id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    if not rutina.es_defecto and rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta rutina")

    # Verifica que el ejercicio pertenezca a esa rutina
    rutina_ej = session.get(RutinaEjercicio, rutina_ejercicio_id)
    if not rutina_ej or rutina_ej.rutina_id != rutina_id:
        raise HTTPException(status_code=404, detail="Ejercicio no pertenece a esta rutina")

    series = session.exec(
        select(RutinaSerie).where(RutinaSerie.rutina_ejercicio_id == rutina_ejercicio_id).order_by(RutinaSerie.numero)
    ).all()

    return series