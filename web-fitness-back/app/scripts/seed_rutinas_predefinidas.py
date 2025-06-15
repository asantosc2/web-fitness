from sqlmodel import Session
from app.db import engine
from app.models import Rutina, RutinaEjercicio, RutinaSerie

with Session(engine) as session:
    # --- RUTINA 1: Torso Básico ---
    torso = Rutina(
        nombre="Torso Básico",
        descripcion="Rutina predefinida de empuje y tracción para el tren superior",
        usuario_id=None,
        es_defecto=True
    )
    session.add(torso)
    session.commit()
    session.refresh(torso)

    ejercicios_torso = [
        {"ejercicio_id": 21, "orden": 1, "series": 3, "repeticiones": 10},
        {"ejercicio_id": 11, "orden": 2, "series": 3, "repeticiones": 10},
        {"ejercicio_id": 5,  "orden": 3, "series": 3, "repeticiones": 12},
        {"ejercicio_id": 6,  "orden": 4, "series": 3, "repeticiones": 12},
    ]

    for ej in ejercicios_torso:
        rutina_ej = RutinaEjercicio(**ej, rutina_id=torso.id)
        session.add(rutina_ej)
        session.flush()  # Necesario para obtener rutina_ej.id

        for i in range(1, ej["series"] + 1):
            session.add(RutinaSerie(
                rutina_ejercicio_id=rutina_ej.id,
                numero=i,
                repeticiones=ej["repeticiones"],
                peso=0.0  # Peso inicial por defecto
            ))

    # --- RUTINA 2: Pierna Básica ---
    pierna = Rutina(
        nombre="Pierna Básica",
        descripcion="Rutina predefinida para trabajar cuádriceps, glúteos y femorales",
        usuario_id=None,
        es_defecto=True
    )
    session.add(pierna)
    session.commit()
    session.refresh(pierna)

    ejercicios_pierna = [
        {"ejercicio_id": 41, "orden": 1, "series": 4, "repeticiones": 10},
        {"ejercicio_id": 45, "orden": 2, "series": 3, "repeticiones": 12},
        {"ejercicio_id": 47, "orden": 3, "series": 3, "repeticiones": 12},
        {"ejercicio_id": 50, "orden": 4, "series": 3, "repeticiones": 15},
    ]

    for ej in ejercicios_pierna:
        rutina_ej = RutinaEjercicio(**ej, rutina_id=pierna.id)
        session.add(rutina_ej)
        session.flush()

        for i in range(1, ej["series"] + 1):
            session.add(RutinaSerie(
                rutina_ejercicio_id=rutina_ej.id,
                numero=i,
                repeticiones=ej["repeticiones"],
                peso=0.0
            ))

    session.commit()

print("✅ Rutinas predefinidas creadas correctamente con series detalladas.")
