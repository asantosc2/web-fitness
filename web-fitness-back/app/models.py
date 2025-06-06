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
    imagen_url: Optional[str] = None
    video_url: Optional[str] = None
    descripcion: Optional[str] = None
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

class Rutina(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    es_defecto: bool = False

    # Relaciones
    ejercicios: List["RutinaEjercicio"] = Relationship(back_populates="rutina")

class RutinaEjercicio(SQLModel, table=True):
    __tablename__ = "rutina_ejercicio"
    id: Optional[int] = Field(default=None, primary_key=True)
    rutina_id: int = Field(foreign_key="rutina.id")
    ejercicio_id: int = Field(foreign_key="ejercicio.id")
    orden: int
    series: int
    repeticiones: int

    # Relaciones inversas
    rutina: Optional[Rutina] = Relationship(back_populates="ejercicios")
    ejercicio: Optional[Ejercicio] = Relationship()


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

class Progreso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: date
    peso: float
    comentarios: Optional[str] = None
    foto_url: Optional[str] = None

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
    fibra_100g: Optional[float] = None
    imagen_url: Optional[str] = None
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")