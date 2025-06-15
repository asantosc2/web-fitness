#sesiones.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import date
from app.models import RutinaSerie, Sesion, RutinaEjercicio, SesionEjercicio, SesionSerie, Usuario
from app.schemas import SesionCreate, SesionEjercicioCreate, SesionEjercicioUpdate, SesionRead, SesionEjercicioRead, SesionSerieRead, SesionSerieCreate, SesionSerieUpdate
from app.dependencies import get_current_user, get_session
from sqlalchemy.orm import selectinload

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

    # 🔹 Obtener ejercicios de la rutina seleccionada
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
            session.flush()  # Necesario para tener copia.id

            # 🔹 Copiar también las series detalladas
            series_originales = session.exec(
                select(RutinaSerie).where(RutinaSerie.rutina_ejercicio_id == e.id)
            ).all()

            for s in series_originales:
                nueva_serie = SesionSerie(
                    sesion_ejercicio_id=copia.id,
                    numero=s.numero,
                    repeticiones=s.repeticiones,
                    peso=s.peso
                )
                session.add(nueva_serie)

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

# 🔹 Ver series detalladas de un ejercicio en una sesión
@router.get("/sesion-ejercicio/{id}/series", response_model=List[SesionSerieRead])
def listar_series_de_ejercicio(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(SesionEjercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    sesion = session.get(Sesion, ejercicio.sesion_id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver las series")

    series = session.exec(
        select(SesionSerie).where(SesionSerie.sesion_ejercicio_id == id).order_by(SesionSerie.numero)
    ).all()

    return series

# 🔹 Editar una serie de una sesión
@router.put("/sesion-serie/{id}", response_model=SesionSerieRead)
def actualizar_serie_sesion(
    id: int,
    datos: SesionSerieCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    serie = session.get(SesionSerie, id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    sesion_ejercicio = session.get(SesionEjercicio, serie.sesion_ejercicio_id)
    if not sesion_ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    sesion = session.get(Sesion, sesion_ejercicio.sesion_id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta sesión")

    serie.numero = datos.numero
    serie.repeticiones = datos.repeticiones
    serie.peso = datos.peso

    session.add(serie)
    session.commit()
    session.refresh(serie)
    return serie

# 🔹 Ver series de un ejercicio de sesión
@router.get("/sesion-ejercicio/{id}/series", response_model=List[SesionSerieRead])
def obtener_series_de_sesion_ejercicio(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(SesionEjercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    sesion = session.get(Sesion, ejercicio.sesion_id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta sesión")

    series = session.exec(
        select(SesionSerie).where(SesionSerie.sesion_ejercicio_id == id).order_by(SesionSerie.numero)
    ).all()

    return series

from app.schemas import SesionSerieCreate, SesionSerieRead

@router.post("/sesion-ejercicio/{id}/series", response_model=List[SesionSerieRead])
def agregar_series_a_ejercicio_de_sesion(
    id: int,
    nuevas_series: List[SesionSerieCreate],
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    ejercicio = session.get(SesionEjercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    sesion = session.get(Sesion, ejercicio.sesion_id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta sesión")

    nuevas = []
    for data in nuevas_series:
        serie = SesionSerie(**data.dict(), sesion_ejercicio_id=id)
        session.add(serie)
        nuevas.append(serie)

    session.commit()
    for s in nuevas:
        session.refresh(s)

    return nuevas

from app.schemas import SesionSerieUpdate

@router.put("/sesion-serie/{id}", response_model=SesionSerieRead)
def actualizar_serie_sesion(
    id: int,
    datos: SesionSerieUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    serie = session.get(SesionSerie, id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    sesion_ejercicio = session.get(SesionEjercicio, serie.sesion_ejercicio_id)
    sesion = session.get(Sesion, sesion_ejercicio.sesion_id) if sesion_ejercicio else None
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta serie")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(serie, campo, valor)

    session.add(serie)
    session.commit()
    session.refresh(serie)
    return serie

@router.delete("/sesion-serie/{id}", status_code=204)
def eliminar_serie_sesion(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    serie = session.get(SesionSerie, id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    ejercicio = session.get(SesionEjercicio, serie.sesion_ejercicio_id)
    sesion = session.get(Sesion, ejercicio.sesion_id) if ejercicio else None
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta serie")

    session.delete(serie)
    session.commit()
    return {"mensaje": f"Serie con ID {id} eliminada correctamente"}
