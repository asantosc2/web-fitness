from fastapi import Depends, HTTPException, Header
from sqlmodel import Session, select
from app.db import get_session
from app.auth import verificar_token
from app.models import Usuario

def get_current_user(
    token: str = Header(..., alias="Authorization"),
    session: Session = Depends(get_session)) -> Usuario:
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de token inválido")
    
    token = token.split(" ")[1]  
    user_id = verificar_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    usuario = session.get(Usuario, int(user_id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
