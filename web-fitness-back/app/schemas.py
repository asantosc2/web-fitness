from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import date, datetime
from app.validators import validar_nombre_apellido, validar_email, validar_password_segura, validar_fecha_nacimiento

# Clase que define el esquema para crear un usuario
class UsuarioCreate(BaseModel):
    # Campos obligatorios del usuario
    nombre: str
    apellido: str
    email: str
    hashed_password: str
    fecha_nacimiento: date

    # Validación para asegurar que los campos no estén vacíos y cumplen con restricciones comunes
    @field_validator("nombre", "apellido", "email", "hashed_password", mode="before")
    def validar_campos_comunes(cls, value, info):
        if value is None or value.strip() == "":
            raise ValueError(f"El campo {info.field_name} es obligatorio y no puede estar vacío")
        return value

    @field_validator("email", mode="before")
    def validar_email(cls, value):
        return validar_email(value)

    # Validación de la seguridad de la contraseña
    @field_validator("hashed_password", mode="before")
    def validar_password_segura(cls, value):
        return validar_password_segura(value)

    # Validación de la fecha de nacimiento
    @field_validator("fecha_nacimiento", mode="before")
    def validar_fecha_nacimiento(cls, value):
        return validar_fecha_nacimiento(value)

    @field_validator("nombre", "apellido", mode="before")
    def validar_nombre_apellido(cls, value, info):
        return validar_nombre_apellido(value, info.field_name)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

    @field_validator("nombre", "apellido", mode="before")
    def validar_nombre_apellido(cls, value, info):
        return validar_nombre_apellido(value, info.field_name)

    @field_validator("email", mode="before")
    def validar_email(cls, value):
        return validar_email(value)

    @field_validator("hashed_password", mode="before")
    def validar_password_segura(cls, value):
        return validar_password_segura(value)

    @field_validator("fecha_nacimiento", mode="before")
    def validar_fecha_nacimiento(cls, value):
        return validar_fecha_nacimiento(value)


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    fecha_nacimiento: date
    fecha_registro: datetime

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: str
    password: str

class RecuperarPasswordRequest(BaseModel):
    email: str

class RestablecerPasswordRequest(BaseModel):
    token: str
    nueva_password: str

class EjercicioBase(BaseModel):
    nombre: str
    grupo_muscular: str
    tipo_equipo: str
    imagen_url: Optional[str] = None
    video_url: Optional[str] = None
    descripcion: Optional[str] = None

class EjercicioCreate(EjercicioBase):
    pass

class EjercicioRead(EjercicioBase):
    id: int
    usuario_id: Optional[int]

    class Config:
        from_attributes = True

class EjercicioUpdate(BaseModel):
    nombre: Optional[str] = None
    grupo_muscular: Optional[str] = None
    tipo_equipo: Optional[str] = None
    imagen_url: Optional[str] = None
    video_url: Optional[str] = None
    descripcion: Optional[str] = None

# Crear rutina (entrada del usuario)
class RutinaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return v

# Leer rutina (respuesta al frontend)
class RutinaRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    usuario_id: Optional[int]
    fecha_creacion: datetime
    es_defecto: bool

    class Config:
        from_attributes = True

# Actualizar rutina
class RutinaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

# Crear asociación ejercicio → rutina
class RutinaEjercicioCreate(BaseModel):
    ejercicio_id: int
    orden: int
    series: int
    repeticiones: int
    comentarios: Optional[str] = None

    @field_validator("orden", "series", "repeticiones")
    @classmethod
    def mayores_que_cero(cls, v):
        if v < 1:
            raise ValueError("El valor debe ser mayor que cero")
        return v   

# Leer la asociación
class RutinaEjercicioRead(BaseModel):
    id: int
    rutina_id: int
    ejercicio_id: int
    orden: int
    series: int
    repeticiones: int
    comentarios: Optional[str] = None

    class Config:
        from_attributes = True

# Actualizar una fila concreta
class RutinaEjercicioUpdate(BaseModel):
    orden: Optional[int] = None
    series: Optional[int] = None
    repeticiones: Optional[int] = None
    comentarios: Optional[str] = None

class SesionCreate(BaseModel):
    rutina_id: Optional[int] = None
    nota: Optional[str] = None

class SesionRead(BaseModel):
    id: int
    usuario_id: int
    fecha: date
    rutina_id: Optional[int]
    nota: Optional[str]

    class Config:
        from_attributes = True


# --- SESION EJERCICIO ---

class SesionEjercicioCreate(BaseModel):
    ejercicio_id: int
    orden: int
    series: int
    repeticiones: int
    peso: float
    comentarios: Optional[str] = None

class SesionEjercicioRead(BaseModel):
    id: int
    sesion_id: int
    ejercicio_id: int
    orden: int
    series: int
    repeticiones: int
    peso: float
    comentarios: Optional[str] = None

    class Config:
        from_attributes = True

class SesionEjercicioUpdate(BaseModel):
    orden: Optional[int] = None
    series: Optional[int] = None
    repeticiones: Optional[int] = None
    peso: Optional[float] = None
    comentarios: Optional[str] = None
