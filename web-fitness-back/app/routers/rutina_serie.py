from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import RutinaEjercicio, RutinaSerie, Usuario
from app.dependencies import get_session, get_current_user
from app.schemas import RutinaSerieCreate, RutinaSerieRead

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
