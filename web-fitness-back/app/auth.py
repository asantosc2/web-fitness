from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

# Configuración del hasheo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret y configuración del JWT
SECRET_KEY = "supersecreto"  # ⚠️ Cámbialo por una variable de entorno en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Verifica si una contraseña plana coincide con el hash
def verificar_password(password_plana: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plana, password_hash)

# Hashea una contraseña nueva
def hashear_password(password_plana: str) -> str:
    return pwd_context.hash(password_plana)

# Crea el token JWT a partir de los datos del usuario
def crear_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verifica el token y devuelve el 'sub' (user_id)
def verificar_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub")) if "sub" in payload else None
    except JWTError:
        return None