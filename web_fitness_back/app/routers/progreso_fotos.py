from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from app.db import get_session
from app.dependencies import get_current_user
from app.models import Progreso, ProgresoFoto
from typing import List
import shutil
import os
import uuid
from app.schemas import ProgresoFotoRead

router = APIRouter(prefix="/progresos", tags=["Fotos Progreso"])

# Ruta donde guardar las fotos localmente
CARPETA_FOTOS = "progreso_fotos"
os.makedirs(CARPETA_FOTOS, exist_ok=True)

@router.post("/{progreso_id}/fotos", response_model=List[ProgresoFotoRead])
def subir_fotos_progreso(
    progreso_id: int,
    archivos: List[UploadFile] = File(...),
    session: Session = Depends(get_session),
    usuario=Depends(get_current_user)
):
    print(f"📸 Recibiendo fotos para progreso {progreso_id}")
    progreso = session.get(Progreso, progreso_id)
    if not progreso or progreso.usuario_id != usuario.id:
        print("❌ Progreso no encontrado o no autorizado")
        raise HTTPException(status_code=404, detail="Progreso no encontrado")

    existentes = session.exec(select(ProgresoFoto).where(ProgresoFoto.progreso_id == progreso_id)).all()
    print(f"🖼️ Ya existen {len(existentes)} fotos")

    if len(existentes) + len(archivos) > 10:
        print("🚫 Se superarían las 10 fotos permitidas")
        raise HTTPException(status_code=400, detail="Máximo de 10 fotos por progreso")

    nuevas_fotos = []

    for archivo in archivos:
        extension = os.path.splitext(archivo.filename)[-1].lower()
        if extension not in [".jpg", ".jpeg", ".png", ".webp"]:
            print(f"❌ Formato inválido: {extension}")
            raise HTTPException(status_code=400, detail="Formato de imagen no permitido")

        nombre_archivo = f"{uuid.uuid4()}{extension}"
        ruta_final = os.path.join(CARPETA_FOTOS, nombre_archivo)

        print(f"➡️ Guardando en: {ruta_final}")
        with open(ruta_final, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)

        nueva_foto = ProgresoFoto(progreso_id=progreso_id, ruta=nombre_archivo)
        session.add(nueva_foto)
        nuevas_fotos.append(nueva_foto)

    session.commit()
    for f in nuevas_fotos:
        session.refresh(f)

    print(f"✅ {len(nuevas_fotos)} fotos guardadas correctamente")
    return nuevas_fotos

@router.delete("/fotos/{foto_id}", status_code=204)
def eliminar_foto_progreso(
    foto_id: int,
    session: Session = Depends(get_session),
    usuario=Depends(get_current_user)
):
    foto = session.get(ProgresoFoto, foto_id)
    if not foto or not foto.progreso or foto.progreso.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="Foto no encontrada o sin permiso")

    # Borrar archivo físico si existe
    ruta_foto = os.path.join(CARPETA_FOTOS, foto.ruta)
    if os.path.isfile(ruta_foto):
        os.remove(ruta_foto)

    session.delete(foto)
    session.commit()
