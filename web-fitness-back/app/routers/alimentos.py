#alimentos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.schemas import AlimentoCreate, AlimentoRead, AlimentoUpdate
from app.models import Alimento
from app.dependencies import get_current_user
from app.services.openfood import buscar_alimentos_openfood

router = APIRouter(prefix="/alimentos", tags=["Alimentos"])

# Búsqueda en OpenFood
@router.get("/buscar-openfood")
async def buscar_openfood(query: str):
    return await buscar_alimentos_openfood(query)


@router.post("/desde-openfood", response_model=AlimentoRead)
def guardar_desde_openfood(data: AlimentoCreate, session: Session = Depends(get_session), usuario=Depends(get_current_user)):
    alimento = Alimento(**data.dict(), usuario_id=usuario.id)
    session.add(alimento)
    session.commit()
    session.refresh(alimento)
    return alimento

@router.post("", response_model=AlimentoRead)
def crear_alimento(data: AlimentoCreate, session: Session = Depends(get_session), usuario=Depends(get_current_user)):
    alimento = Alimento(**data.dict(), usuario_id=usuario.id)
    session.add(alimento)
    session.commit()
    session.refresh(alimento)
    return alimento

@router.get("", response_model=list[AlimentoRead])
def listar_alimentos(session: Session = Depends(get_session), usuario=Depends(get_current_user)):
    return session.exec(select(Alimento).where(Alimento.usuario_id == usuario.id)).all()

@router.get("/{alimento_id}", response_model=AlimentoRead)
def obtener_alimento(alimento_id: int, session: Session = Depends(get_session), usuario=Depends(get_current_user)):
    alimento = session.get(Alimento, alimento_id)
    if not alimento or alimento.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return alimento

@router.put("/{alimento_id}", response_model=AlimentoRead)
def actualizar_alimento(alimento_id: int, data: AlimentoUpdate, session: Session = Depends(get_session), usuario=Depends(get_current_user)):
    alimento = session.get(Alimento, alimento_id)
    if not alimento or alimento.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="No encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(alimento, key, value)

    session.commit()
    session.refresh(alimento)
    return alimento

@router.delete("/{alimento_id}", status_code=204)
def eliminar_alimento(alimento_id: int, session: Session = Depends(get_session), usuario=Depends(get_current_user)):
    alimento = session.get(Alimento, alimento_id)
    if not alimento or alimento.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="No encontrado")
    session.delete(alimento)
    session.commit()
    return


