# sesiones.py
import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import date
from app.models import RutinaSerie, Sesion, Rutina, RutinaEjercicio, SesionEjercicio, SesionSerie, Usuario
from app.schemas import (
    SesionCreate, SesionEjercicioCreate, SesionEjercicioUpdate,
    SesionRead, SesionEjercicioRead, SesionSerieRead,
    SesionSerieCreate, SesionSerieUpdate
)
from app.dependencies import get_current_user, get_session
from sqlalchemy.orm import selectinload

router = APIRouter(tags=["Sesion"])

@router.get("/sesiones", response_model=List[SesionRead])
def listar_sesiones(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    sesiones = session.exec(
        select(Sesion)
        .where(Sesion.usuario_id == current_user.id)
        .order_by(Sesion.fecha.desc())
        .options(selectinload(Sesion.rutina))
    ).all()

    resultado = []
    for s in sesiones:
        data = SesionRead.model_validate(s, from_attributes=True)
        data.nombre_rutina = s.rutina.nombre if s.rutina else None
        resultado.append(data)

    return resultado

@router.post("/sesiones", response_model=SesionRead)
def crear_sesion(
    sesion_data: SesionCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        nueva_sesion = Sesion(
            usuario_id=current_user.id,
            fecha=date.today(),
            rutina_id=sesion_data.rutina_id,
        )
        session.add(nueva_sesion)
        session.commit()
        session.refresh(nueva_sesion)
        nueva_sesion = session.exec(
            select(Sesion)
            .where(Sesion.id == nueva_sesion.id)
            .options(selectinload(Sesion.rutina))
        ).first()

        nombre_rutina = nueva_sesion.rutina.nombre if nueva_sesion.rutina else None

        resultado = SesionRead.model_validate(nueva_sesion, from_attributes=True)
        resultado.nombre_rutina = nombre_rutina

        if sesion_data.rutina_id:
            ejercicios = session.exec(
                select(RutinaEjercicio).where(RutinaEjercicio.rutina_id == sesion_data.rutina_id)
            ).all()

            print(f"▶ Rutina {sesion_data.rutina_id} tiene {len(ejercicios)} ejercicios")

            for e in ejercicios:
                print(f"➕ Copiando ejercicio {e.ejercicio_id} con orden {e.orden}")
                series_originales = session.exec(
                    select(RutinaSerie).where(RutinaSerie.rutina_ejercicio_id == e.id)
                ).all()

                copia = SesionEjercicio(
                    sesion_id=nueva_sesion.id,
                    ejercicio_id=e.ejercicio_id,
                    orden=e.orden,
                    series=len(series_originales),  # ✅ Usamos la longitud de las series
                    repeticiones=series_originales[0].repeticiones if series_originales else 10,
                    peso=0.0,
                    comentarios=e.comentarios
                )
                session.add(copia)
                session.flush()  # Necesario para obtener el ID de la copia


                for s in series_originales:
                    print(f"   🔄 Serie {s.numero}: {s.repeticiones} reps, {s.peso} kg")
                    nueva_serie = SesionSerie(
                        sesion_ejercicio_id=copia.id,
                        numero=s.numero,
                        repeticiones=s.repeticiones,
                        peso=s.peso
                    )
                    session.add(nueva_serie)

        session.commit()
        return resultado
    except Exception as err:
        print("❌ Error interno al crear la sesión:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error interno al crear la sesión")


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

    # 🔁 ACTUALIZAR también los valores en RutinaEjercicio si aplica
    if sesion.rutina_id:
        rutina_ejercicio = session.exec(
            select(RutinaEjercicio).where(
                RutinaEjercicio.rutina_id == sesion.rutina_id,
                RutinaEjercicio.ejercicio_id == ejercicio.ejercicio_id
            )
        ).first()
        if rutina_ejercicio:
            rutina_ejercicio.peso = ejercicio.peso
            rutina_ejercicio.series = ejercicio.series
            rutina_ejercicio.repeticiones = ejercicio.repeticiones
            session.add(rutina_ejercicio)
            session.commit()

    return ejercicio

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

    # 🔄 ELIMINAR SERIES ASOCIADAS PRIMERO (por si no hay cascade en la relación)
    series = session.exec(
        select(SesionSerie).where(SesionSerie.sesion_ejercicio_id == ejercicio.id)
    ).all()
    for s in series:
        session.delete(s)

    session.delete(ejercicio)
    session.commit()
    return {"mensaje": f"Ejercicio con ID {id} eliminado correctamente"}


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

@router.get("/sesiones/{id}/ejercicios", response_model=List[SesionEjercicioRead])
def listar_ejercicios_de_sesion(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    sesion = session.get(Sesion, id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    if sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta sesión")

    ejercicios = session.exec(
        select(SesionEjercicio)
        .where(SesionEjercicio.sesion_id == id)
        .order_by(SesionEjercicio.orden)
        .options(selectinload(SesionEjercicio.ejercicio))  # Carga datos del ejercicio
    ).all()
    return ejercicios


@router.post("/sesiones/{id}/actualizar-rutina")
def actualizar_rutina_desde_sesion(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    sesion = session.get(Sesion, id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta sesión")

    if not sesion.rutina_id:
        raise HTTPException(status_code=400, detail="Esta sesión no está vinculada a ninguna rutina")

    rutina = session.get(Rutina, sesion.rutina_id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina asociada no encontrada")

    # 🔁 1. Eliminar ejercicios y series anteriores de la rutina
    ejercicios_anteriores = session.exec(
        select(RutinaEjercicio).where(RutinaEjercicio.rutina_id == rutina.id)
    ).all()

    for re in ejercicios_anteriores:
        series = session.exec(
            select(RutinaSerie).where(RutinaSerie.rutina_ejercicio_id == re.id)
        ).all()
        for s in series:
            session.delete(s)
        session.delete(re)

    session.commit()

    # ➕ 2. Copiar los nuevos ejercicios desde la sesión
    ejercicios_sesion = session.exec(
        select(SesionEjercicio).where(SesionEjercicio.sesion_id == sesion.id)
    ).all()

    for ej in ejercicios_sesion:
        nuevo = RutinaEjercicio(
            rutina_id=rutina.id,
            ejercicio_id=ej.ejercicio_id,
            orden=ej.orden,
            comentarios=ej.comentarios
        )
        session.add(nuevo)
        session.flush()

        series = session.exec(
            select(SesionSerie).where(SesionSerie.sesion_ejercicio_id == ej.id)
        ).all()

        for s in series:
            nueva_serie = RutinaSerie(
                rutina_ejercicio_id=nuevo.id,
                numero=s.numero,
                repeticiones=s.repeticiones,
                peso=s.peso
            )
            session.add(nueva_serie)

    session.commit()

    return {"mensaje": "Rutina actualizada correctamente desde la sesión"}

@router.delete("/sesiones/{id}", status_code=204)
def eliminar_sesion_completa(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    sesion = session.get(Sesion, id)
    if not sesion or sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta sesión")

    session.delete(sesion)
    session.commit()
    return {"mensaje": f"Sesión con ID {id} eliminada correctamente"}

@router.put("/sesiones/{id}/orden-ejercicios")
def actualizar_orden_sesion_ejercicios(
    id: int,
    orden_data: list[dict],
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    sesion = session.get(Sesion, id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    if sesion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    for item in orden_data:
        sesion_ejercicio_id = item.get("sesion_ejercicio_id")
        nuevo_orden = item.get("nuevo_orden")
        if sesion_ejercicio_id is None or nuevo_orden is None:
            continue

        ejercicio = session.get(SesionEjercicio, sesion_ejercicio_id)
        if ejercicio and ejercicio.sesion_id == sesion.id:
            ejercicio.orden = nuevo_orden
            session.add(ejercicio)

    session.commit()
    return {"message": "Orden actualizado correctamente"}
