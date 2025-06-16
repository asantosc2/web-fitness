import re
from datetime import date
from sqlmodel import Session, select
from app.db import engine
from app.models import Usuario

def validar_nombre_apellido(value: str, field_name: str) -> str:
    if not value.isalpha():
        raise ValueError(f"El campo {field_name} solo puede contener letras")
    if len(value) > 50:
        raise ValueError(f"El campo {field_name} no puede exceder los 50 caracteres")
    return value

def validar_email(value: str) -> str:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValueError("El correo electrónico no es válido")
    if len(value) > 100:
        raise ValueError("El email no puede exceder los 100 caracteres")
    with Session(engine) as session:
        existente = session.exec(select(Usuario).where(Usuario.email == value)).first()
        if existente:
            raise ValueError("El correo electrónico ya está registrado")
    return value

def validar_password_segura(value: str) -> str:
    if len(value) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    if not re.search(r"[A-Z]", value):
        raise ValueError("Debe contener al menos una letra mayúscula")
    if not re.search(r"[a-z]", value):
        raise ValueError("Debe contener al menos una letra minúscula")
    if not re.search(r"[0-9]", value):
        raise ValueError("Debe contener al menos un número")
    if not re.search(r"[^A-Za-z0-9]", value):
        raise ValueError("Debe contener al menos un carácter especial")
    contraseñas_comunes = ["123456", "password", "12345678", "qwerty", "abc123"]
    if value.lower() in contraseñas_comunes:
        raise ValueError("La contraseña es demasiado común y no es segura")
    return value

from datetime import date

def validar_fecha_nacimiento(value):
    if value is None:
        raise ValueError("La fecha de nacimiento es obligatoria")

    if isinstance(value, str):
        try:
            value = date.fromisoformat(value)
        except ValueError:
            raise ValueError("La fecha de nacimiento debe estar en formato YYYY-MM-DD")

    hoy = date.today()
    if value > hoy:
        raise ValueError("La fecha de nacimiento no puede ser futura")

    edad_minima = 16
    edad = hoy.year - value.year - ((hoy.month, hoy.day) < (value.month, value.day))
    if edad < edad_minima:
        raise ValueError(f"El usuario debe tener al menos {edad_minima} años")

    return value
