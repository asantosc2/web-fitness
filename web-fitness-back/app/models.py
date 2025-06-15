#models.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime
from typing import Optional, List

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str
    hashed_password: str
    fecha_nacimiento: date
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    is_admin: bool = Field(default=False)
    token_recuperacion: Optional[str] = Field(default=None, index=True)
    token_expira: Optional[datetime] = None

class Ejercicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    grupo_muscular: str
    tipo_equipo: str     
    descripcion: Optional[str] = None
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

    fotos: List["EjercicioFoto"] = Relationship(back_populates="ejercicio")

class EjercicioFoto(SQLModel, table=True):
    __tablename__ = "ejercicio_foto"
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    ejercicio_id: int = Field(foreign_key="ejercicio.id")
    ejercicio: Optional["Ejercicio"] = Relationship(back_populates="fotos")

class Rutina(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = Field(default=None, nullable=True)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    es_defecto: bool = False

    ejercicios: List["RutinaEjercicio"] = Relationship(
        back_populates="rutina",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class RutinaEjercicio(SQLModel, table=True):
    __tablename__ = "rutina_ejercicio"
    id: Optional[int] = Field(default=None, primary_key=True)
    rutina_id: int = Field(foreign_key="rutina.id")
    ejercicio_id: int = Field(foreign_key="ejercicio.id")
    orden: int
    comentarios: Optional[str] = Field(default=None)

    rutina: Optional[Rutina] = Relationship(back_populates="ejercicios")
    ejercicio: Optional["Ejercicio"] = Relationship()

    series_detalle: List["RutinaSerie"] = Relationship(
        back_populates="rutina_ejercicio",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class RutinaSerie(SQLModel, table=True):
    __tablename__ = "rutina_serie"
    id: Optional[int] = Field(default=None, primary_key=True)
    rutina_ejercicio_id: int = Field(foreign_key="rutina_ejercicio.id")
    numero: int  
    repeticiones: int
    peso: float

    rutina_ejercicio: Optional[RutinaEjercicio] = Relationship(back_populates="series_detalle")

class Sesion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: date
    rutina_id: Optional[int] = Field(default=None, foreign_key="rutina.id")
    nota: Optional[str] = None

    ejercicios: List["SesionEjercicio"] = Relationship(back_populates="sesion")


class SesionEjercicio(SQLModel, table=True):
    __tablename__ = "sesion_ejercicio"
    id: Optional[int] = Field(default=None, primary_key=True)
    sesion_id: int = Field(foreign_key="sesion.id")
    ejercicio_id: int = Field(foreign_key="ejercicio.id")
    orden: int
    series: int
    repeticiones: int
    peso: float
    comentarios: Optional[str] = None

    sesion: Optional[Sesion] = Relationship(back_populates="ejercicios")
    ejercicio: Optional[Ejercicio] = Relationship()

class SesionSerie(SQLModel, table=True):
    __tablename__ = "sesion_serie"
    id: Optional[int] = Field(default=None, primary_key=True)
    sesion_ejercicio_id: int = Field(foreign_key="sesion_ejercicio.id")
    numero: int
    repeticiones: int
    peso: float

class Progreso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: date
    peso: float
    comentarios: Optional[str] = None

    fotos: List["ProgresoFoto"] = Relationship(
    back_populates="progreso",
    sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class ProgresoFoto(SQLModel, table=True):
    __tablename__ = "progreso_foto"
    id: Optional[int] = Field(default=None, primary_key=True)
    progreso_id: int = Field(foreign_key="progreso.id")
    ruta: str

    progreso: Optional[Progreso] = Relationship(back_populates="fotos")

class Dieta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    nombre: str
    descripcion: Optional[str] = None

    comidas: List["Comida"] = Relationship(back_populates="dieta")

class Comida(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dieta_id: int = Field(foreign_key="dieta.id")
    nombre: str

    dieta: Optional[Dieta] = Relationship(back_populates="comidas")
    alimentos: List["ComidaAlimento"] = Relationship(back_populates="comida")

class ComidaAlimento(SQLModel, table=True):
    __tablename__ = "comida_alimento"
    id: Optional[int] = Field(default=None, primary_key=True)
    comida_id: int = Field(foreign_key="comida.id")
    alimento_id: int = Field(foreign_key="alimento.id")
    porcion: str
    calorias: float
    proteinas: float
    carbohidratos: float
    grasas: float

    comida: Optional[Comida] = Relationship(back_populates="alimentos")
    alimento: Optional["Alimento"] = Relationship()

class Alimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    calorias_100g: float
    proteinas_100g: float
    carbohidratos_100g: float
    grasas_100g: float
    imagen_url: Optional[str] = None
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")