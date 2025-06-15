#rutina_serie.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import Rutina, RutinaEjercicio, RutinaSerie, Usuario
from app.dependencies import get_session, get_current_user
from app.schemas import RutinaSerieCreate, RutinaSerieRead, RutinaSerieUpdate

router = APIRouter(tags=["Rutina Serie"])

# 🔹 Listar todas las series de un ejercicio de rutina
@router.get("/rutina-ejercicio/{id}/series", response_model=List[RutinaSerieRead])
def listar_series_de_rutina_ejercicio(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(RutinaEjercicio, id)
    if not ejercicio or ejercicio.rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver estas series")

    return ejercicio.series_detalle

# 🔹 Añadir series a un ejercicio de rutina
@router.post("/rutina-ejercicio/{id}/series", response_model=List[RutinaSerieRead])
def agregar_series_a_rutina_ejercicio(
    id: int,
    series: List[RutinaSerieCreate],
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(RutinaEjercicio, id)
    if not ejercicio or ejercicio.rutina.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta rutina")

    nuevas = []
    for serie in series:
        nueva = RutinaSerie(
            rutina_ejercicio_id=id,
            numero=serie.numero,
            repeticiones=serie.repeticiones,
            peso=serie.peso
        )
        session.add(nueva)
        nuevas.append(nueva)

    session.commit()
    for s in nuevas:
        session.refresh(s)

    return nuevas

@router.put("/rutina-serie/{id}", response_model=RutinaSerieRead)
def actualizar_serie(
    id: int,
    datos: RutinaSerieUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    serie = session.get(RutinaSerie, id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    rutina_ej = session.get(RutinaEjercicio, serie.rutina_ejercicio_id)
    rutina = session.get(Rutina, rutina_ej.rutina_id)

    if not rutina or (not rutina.es_defecto and rutina.usuario_id != current_user.id):
        raise HTTPException(status_code=403, detail="No tienes permiso")

    # Solo actualiza si se ha enviado
    if datos.peso is not None:
        serie.peso = datos.peso
    if datos.repeticiones is not None:
        serie.repeticiones = datos.repeticiones

    session.add(serie)
    session.commit()
    session.refresh(serie)
    return serie

@router.delete("/rutina-serie/{id}", status_code=204)
def eliminar_serie(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    serie = session.get(RutinaSerie, id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    rutina_ej = session.get(RutinaEjercicio, serie.rutina_ejercicio_id)
    rutina = session.get(Rutina, rutina_ej.rutina_id)

    if not rutina or (not rutina.es_defecto and rutina.usuario_id != current_user.id):
        raise HTTPException(status_code=403, detail="No tienes permiso")

    session.delete(serie)
    session.commit()
    return {"mensaje": f"Serie con ID {id} eliminada correctamente"}
