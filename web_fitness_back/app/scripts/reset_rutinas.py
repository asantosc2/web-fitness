# app/scripts/reset_rutinas.py

from sqlmodel import Session
from app.db import engine
from sqlalchemy import text
from app.models import Rutina, RutinaEjercicio

def reset_rutinas():
    print("⚠️ Eliminando rutinas y reiniciando secuencia de ID...")

    with Session(engine) as session:
        session.exec(text("DELETE FROM rutina_ejercicio;"))
        session.exec(text("DELETE FROM rutina;"))
        session.exec(text("ALTER SEQUENCE rutina_id_seq RESTART WITH 1;"))
        session.exec(text("ALTER SEQUENCE rutina_ejercicio_id_seq RESTART WITH 1;"))
        session.commit()

    print("✅ Rutinas eliminadas y secuencia reiniciada.")

if __name__ == "__main__":
    reset_rutinas()
