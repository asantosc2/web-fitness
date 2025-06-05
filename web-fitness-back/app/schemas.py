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
    is_admin: bool = False  # Por defecto, los nuevos usuarios no son administradores

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
    nombre: Optional[str]
    apellido: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]
    fecha_nacimiento: Optional[date]

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


class UsuarioSelfUpdate(BaseModel):
    nombre: str
    apellido: str
    hashed_password: str
    fecha_nacimiento: date

    @field_validator("nombre", "apellido", mode="before")
    def validar_nombre_apellido(cls, value, info):
        return validar_nombre_apellido(value, info.field_name)

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