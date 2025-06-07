from sqlmodel import SQLModel, Session
from app.db import engine
from app.models import Usuario, Ejercicio, Rutina, RutinaEjercicio
import hashlib
from datetime import date
from sqlalchemy import text

def hashear_password(password: str) -> str:
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def reset_database():
    print("⚠️ Reiniciando esquema de base de datos...")

    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()

    SQLModel.metadata.create_all(engine)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        print("Insertando datos iniciales...")

        # Usuario administrador
        admin = Usuario(
            nombre="Admin",
            apellido="Test",
            email="admin@example.com",
            hashed_password=hashear_password("Admin123!"),
            fecha_nacimiento=date(1990, 1, 1),
            is_admin=True
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)

        # Usuario normal
        usuario = Usuario(
            nombre="Pablo",
            apellido="Martínez",
            email="pablo@example.com",
            hashed_password=hashear_password("Usuario123!"),
            fecha_nacimiento=date(1995, 6, 15),
            is_admin=False
        )
        session.add(usuario)
        session.commit()
        session.refresh(usuario)

        # Ejercicios públicos
        ejercicio1 = Ejercicio(
            nombre="Press banca",
            grupo_muscular="Pectoral",
            tipo_equipo="Barra",
            descripcion="Túmbate en un banco, baja la barra hasta el pecho y empuja hacia arriba."
        )
        ejercicio2 = Ejercicio(
            nombre="Dominadas",
            grupo_muscular="Espalda",
            tipo_equipo="Peso corporal",
            descripcion="Agarra la barra y elévate hasta que la barbilla supere la barra."
        )
        ejercicio3 = Ejercicio(
            nombre="Sentadilla",
            grupo_muscular="Piernas",
            tipo_equipo="Barra",
            descripcion="Coloca la barra sobre los hombros y baja manteniendo la espalda recta."
        )
        session.add_all([ejercicio1, ejercicio2, ejercicio3])
        session.commit()

        # Rutina pública asociada al admin
        rutina = Rutina(
            nombre="Torso A",
            descripcion="Rutina de fuerza centrada en el tren superior",
            usuario_id=admin.id,
            es_defecto=True
        )
        session.add(rutina)
        session.commit()
        session.refresh(rutina)

        # Asociación rutina-ejercicios
        re1 = RutinaEjercicio(
            rutina_id=rutina.id,
            ejercicio_id=ejercicio1.id,
            orden=1,
            series=4,
            repeticiones=6,
            comentarios="Enfocado a fuerza máxima"
        )
        re2 = RutinaEjercicio(
            rutina_id=rutina.id,
            ejercicio_id=ejercicio2.id,
            orden=2,
            series=3,
            repeticiones=8,
            comentarios="Trabajo complementario de espalda"
        )
        session.add_all([re1, re2])
        session.commit()

    print("Base de datos reiniciada correctamente.")

if __name__ == "__main__":
    reset_database()
