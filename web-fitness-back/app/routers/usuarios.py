from datetime import datetime, timedelta
from typing import List
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Usuario
from app.db import engine
from app.schemas import RecuperarPasswordRequest, RestablecerPasswordRequest, UsuarioCreate, UsuarioLogin, UsuarioRead, UsuarioSelfUpdate, UsuarioUpdate
from fastapi.responses import JSONResponse
from app.auth import crear_token, verificar_password, hashear_password
from app.dependencies import get_current_user
from app.validators import validar_password_segura
from fastapi.responses import JSONResponse
import logging


logger = logging.getLogger("recuperacion")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("recuperacion_tokens.log"),
        logging.StreamHandler()
    ]
)

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/usuarios", response_model=UsuarioRead)
def crear_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    # Verificar si ya existe un usuario con ese email
    usuario_existente = session.exec(select(Usuario).where(Usuario.email == usuario.email)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese email")

    data = usuario.dict()
    data["hashed_password"] = hashear_password(data["hashed_password"])
    nuevo_usuario = Usuario(**data)

    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return nuevo_usuario

@router.put("/usuarios/me", response_model=UsuarioRead)
def actualizar_mis_datos(
    datos: UsuarioUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if datos.email and datos.email != current_user.email:
        # Comprobar que no exista otro usuario con ese email
        existente = session.exec(select(Usuario).where(Usuario.email == datos.email)).first()
        if existente:
            raise HTTPException(status_code=400, detail="Ese email ya está registrado por otro usuario")
    
    for clave, valor in datos.dict(exclude_unset=True).items():
        if clave == "hashed_password":
            valor = hashear_password(valor)
        if clave == "is_admin":
            continue  # No permitimos que el usuario se haga admin
        setattr(current_user, clave, valor)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.delete("/usuarios/me", status_code=204)
def borrar_mi_cuenta(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
        if current_user.is_admin:
            raise HTTPException(status_code=403, detail="Un administrador no puede eliminar su propia cuenta.")
        
        session.delete(current_user)
        session.commit()
        return JSONResponse(status_code=204, content={"mensaje": "Cuenta eliminada correctamente"})

@router.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios(current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Solo el administrador puede ver todos los usuarios")
    usuarios = session.exec(select(Usuario)).all()
    return usuarios

@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(
    usuario_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver otros usuarios")
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden modificar otros usuarios")

    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for clave, valor in datos.dict(exclude_unset=True).items():
        setattr(usuario, clave, valor)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.put("/usuarios/{usuario_id}/perfil", response_model=UsuarioRead)
def actualizar_perfil(usuario_id: int, datos: UsuarioSelfUpdate, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = datos.nombre
    usuario.apellido = datos.apellido
    usuario.hashed_password = datos.hashed_password
    usuario.fecha_nacimiento = datos.fecha_nacimiento

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.delete("/usuarios/{usuario_id}", response_class=JSONResponse)
def eliminar_usuario(
    usuario_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar cuentas ajenas")

    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    session.delete(usuario)
    session.commit()
    return {"mensaje": f"Usuario con ID {usuario_id} eliminado correctamente"}


@router.post("/usuarios/recuperar")
def solicitar_recuperacion(request: RecuperarPasswordRequest, session: Session = Depends(get_session)):
    usuario = session.exec(select(Usuario).where(Usuario.email == request.email)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No se encontró un usuario con ese email")

    token = str(uuid4())
    usuario.token_recuperacion = token
    usuario.token_expira = datetime.utcnow() + timedelta(minutes=30)

    session.add(usuario)
    session.commit()

    logger.info(f"Token de recuperación generado para {usuario.email}: {token}")
    logger.info(f"Enlace de recuperación: https://tufrontend.com/reset-password?token={token}")

    return {"mensaje": "Se ha enviado un enlace de recuperación al correo electrónico"}

@router.post("/usuarios/restablecer")
def restablecer_password(request: RestablecerPasswordRequest, session: Session = Depends(get_session)):
    usuario = session.exec(select(Usuario).where(Usuario.token_recuperacion == request.token)).first()
    if not usuario or not usuario.token_expira or datetime.utcnow() > usuario.token_expira:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    # Validamos la nueva contraseña (reutiliza tus validadores si puedes)
    
    try:
        validar_password_segura(request.nueva_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    usuario.hashed_password = hashear_password(request.nueva_password)
    usuario.token_recuperacion = None
    usuario.token_expira = None

    session.add(usuario)
    session.commit()

    return {"mensaje": "Contraseña actualizada correctamente"}

@router.post("/login")
def login(request: UsuarioLogin, session: Session = Depends(get_session)):
    usuario = session.exec(select(Usuario).where(Usuario.email == request.email)).first()
    if not usuario or not verificar_password(request.hashed_password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = crear_token({"sub": str(usuario.id)})
    return {"access_token": access_token, "token_type": "bearer", "usuario": UsuarioRead.model_validate(usuario)} 

@router.get("/perfil", response_model=UsuarioRead)
def ver_perfil(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.get("/verify-token")
def verificar_token_actual(current_user: Usuario = Depends(get_current_user)):
    return {"valido": True, "usuario": UsuarioRead.model_validate(current_user)}