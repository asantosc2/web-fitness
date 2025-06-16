#schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from app.validators import validar_nombre_apellido, validar_email, validar_password_segura, validar_fecha_nacimiento

# Clase que define el esquema para crear un usuario
class UsuarioCreate(BaseModel):
    # Campos obligatorios del usuario
    nombre: str
    apellido: str
    email: str
    password: str
    fecha_nacimiento: date

    # Validación para asegurar que los campos no estén vacíos y cumplen con restricciones comunes
    @field_validator("nombre", "apellido", "email", "password", mode="before")
    def validar_campos_comunes(cls, value, info):
        if value is None or value.strip() == "":
            raise ValueError(f"El campo {info.field_name} es obligatorio y no puede estar vacío")
        return value

    @field_validator("email", mode="before")
    def validar_email(cls, value):
        return validar_email(value)

    # Validación de la seguridad de la contraseña
    @field_validator("password", mode="before")
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
    password: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

    @field_validator("nombre", "apellido", mode="before")
    def validar_nombre_apellido(cls, value, info):
        return validar_nombre_apellido(value, info.field_name)

    @field_validator("email", mode="before")
    def validar_email(cls, value):
        return validar_email(value)

    @field_validator("password", mode="before")
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


class EjercicioFotoRead(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True

class EjercicioBase(BaseModel):
    nombre: str
    grupo_muscular: str
    tipo_equipo: str
    video_url: Optional[str] = None
    descripcion: Optional[str] = None

class EjercicioCreate(EjercicioBase):
    fotos: Optional[List[str]] = []  # lista de URLs

class EjercicioRead(EjercicioBase):
    id: int
    usuario_id: Optional[int]
    fotos: List[EjercicioFotoRead] = []

    class Config:
        from_attributes = True

class EjercicioUpdate(BaseModel):
    nombre: Optional[str] = None
    grupo_muscular: Optional[str] = None
    tipo_equipo: Optional[str] = None
    video_url: Optional[str] = None
    descripcion: Optional[str] = None
    fotos: Optional[List[str]] = None

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
    comentarios: Optional[str] = None

    @field_validator("orden")
    @classmethod
    def orden_positivo(cls, v):
        if v < 1:
            raise ValueError("El orden debe ser mayor que cero")
        return v

class RutinaOrdenUpdate(BaseModel):
    id: int
    orden: int

# --- Series de una rutina ---
class RutinaSerieCreate(BaseModel):
    numero: int
    repeticiones: int
    peso: float

    @field_validator("numero", "repeticiones", "peso")
    @classmethod
    def validos(cls, v):
        if v <= 0:
            raise ValueError("Los valores deben ser mayores que cero")
        return v

class RutinaSerieRead(BaseModel):
    id: int
    numero: int
    repeticiones: int
    peso: float

    class Config:
        from_attributes = True


# --- Series de una sesión ---
class SesionSerieCreate(BaseModel):
    numero: int
    repeticiones: int
    peso: float

class SesionSerieRead(BaseModel):
    id: int
    numero: int
    repeticiones: int
    peso: float

    class Config:
        from_attributes = True

class RutinaEjercicioRead(BaseModel):
    id: int
    rutina_id: int
    ejercicio_id: int
    orden: int
    comentarios: Optional[str]
    ejercicio: EjercicioRead

    class Config:
        from_attributes = True

class RutinaSerieUpdate(BaseModel):
    peso: Optional[float] = None
    repeticiones: Optional[int] = None


# Actualizar una fila concreta
class RutinaEjercicioUpdate(BaseModel):
    orden: Optional[int] = None
    comentarios: Optional[str] = None

class SesionCreate(BaseModel):
    rutina_id: Optional[int] = None

class SesionRead(BaseModel):
    id: int
    usuario_id: int
    fecha: date
    rutina_id: Optional[int]
    nombre_rutina: Optional[str] = None

    class Config:
        from_attributes = True

class SesionSerieUpdate(BaseModel):
    numero: Optional[int] = None
    repeticiones: Optional[int] = None
    peso: Optional[float] = None

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
    ejercicio: Optional[EjercicioRead]

    class Config:
        from_attributes = True

class SesionEjercicioUpdate(BaseModel):
    orden: Optional[int] = None
    series: Optional[int] = None
    repeticiones: Optional[int] = None
    peso: Optional[float] = None
    comentarios: Optional[str] = None

class AlimentoBase(BaseModel):
    nombre: str
    calorias_100g: float
    proteinas_100g: float
    carbohidratos_100g: float
    grasas_100g: float
    imagen_url: Optional[str] = None

class AlimentoCreate(AlimentoBase):
    pass

class AlimentoUpdate(BaseModel):
    nombre: Optional[str] = None
    calorias_100g: Optional[float] = None
    proteinas_100g: Optional[float] = None
    carbohidratos_100g: Optional[float] = None
    grasas_100g: Optional[float] = None
    imagen_url: Optional[str] = None

class AlimentoRead(AlimentoBase):
    id: int
    imagen_url: Optional[str] = None

    class Config:
        from_attributes = True

class ProgresoFotoRead(BaseModel):
    id: int
    ruta: str  # 🔄 este es el campo real del modelo SQLModel

    class Config:
        from_attributes = True


class ProgresoCreate(BaseModel):
    fecha: date
    peso: float
    comentarios: Optional[str] = None

class ProgresoUpdate(BaseModel):
    peso: Optional[float] = None
    comentarios: Optional[str] = None

class ProgresoRead(BaseModel):
    id: int
    fecha: date
    peso: float
    comentarios: Optional[str]
    fotos: List[ProgresoFotoRead] = []

    class Config:
        from_attributes = True