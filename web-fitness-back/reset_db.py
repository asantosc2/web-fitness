from sqlmodel import SQLModel, create_engine, Session
from app.models import Usuario, Ejercicio, Rutina
from datetime import date

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/web_fitness"
engine = create_engine(DATABASE_URL, echo=True)

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    admin = Usuario(
        nombre="Admin",
        apellido="Fitness",
        email="admin@fitness.com",
        hashed_password = "$2b$12$YQUA85I2MvNnhy.PvZI9oe9M/UtvAbBNhyCV6yD5YNuMm1LHmnI6e",
        fecha_nacimiento=date(1990, 1, 1),
        is_admin=True
    )
    user = Usuario(
        nombre="Usuario",
        apellido="Normal",
        hashed_password = "$2b$12$YQUA85I2MvNnhy.PvZI9oe9M/UtvAbBNhyCV6yD5YNuMm1LHmnI6e",
        email="usuario@fitness.com",
        fecha_nacimiento=date(2000, 6, 6),
        is_admin=False
    )

    session.add_all([admin, user])
    session.commit()

    ejercicios = [
        Ejercicio(nombre="Press Banca", grupo_muscular="Pectoral", tipo_equipo="Barra"),
        Ejercicio(nombre="Dominadas", grupo_muscular="Espalda", tipo_equipo="Peso Corporal"),
        Ejercicio(nombre="Sentadilla", grupo_muscular="Piernas", tipo_equipo="Barra"),
    ]
    session.add_all(ejercicios)
    session.commit()

    rutina = Rutina(
        nombre="Torso Fuerza",
        descripcion="Rutina base para fuerza en torso",
        usuario_id=admin.id,
        es_defecto=True
    )
    session.add(rutina)
    session.commit()
