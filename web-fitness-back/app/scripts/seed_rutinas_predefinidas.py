from sqlmodel import Session
from app.db import engine
from app.models import Rutina, RutinaEjercicio, RutinaSerie

with Session(engine) as session:
    # Crear la rutina
    rutina = Rutina(
        nombre="Push Intermedio",
        descripcion="Entrenamiento de empuje para pecho, hombros y tríceps",
        usuario_id=None,
        es_defecto=True
    )
    session.add(rutina)
    session.commit()
    session.refresh(rutina)

    # Ejercicios con series (peso 0)
    ejercicios = [
        {
            "ejercicio_id": 21,  # Press banca con barra
            "orden": 1,
            "series_detalladas": [
                {"numero": 1, "repeticiones": 8},
                {"numero": 2, "repeticiones": 8},
                {"numero": 3, "repeticiones": 6},
            ]
        },
        {
            "ejercicio_id": 23,  # Press militar con barra
            "orden": 2,
            "series_detalladas": [
                {"numero": 1, "repeticiones": 10},
                {"numero": 2, "repeticiones": 8},
                {"numero": 3, "repeticiones": 8},
            ]
        },
        {
            "ejercicio_id": 31,  # Fondos en paralelas
            "orden": 3,
            "series_detalladas": [
                {"numero": 1, "repeticiones": 12},
                {"numero": 2, "repeticiones": 12},
                {"numero": 3, "repeticiones": 10},
            ]
        }
    ]

    for ej in ejercicios:
        rutina_ej = RutinaEjercicio(
            rutina_id=rutina.id,
            ejercicio_id=ej["ejercicio_id"],
            orden=ej["orden"],
            series=len(ej["series_detalladas"]),
            repeticiones=0  # reps específicas por serie
        )
        session.add(rutina_ej)
        session.flush()

        for serie in ej["series_detalladas"]:
            session.add(RutinaSerie(
                rutina_ejercicio_id=rutina_ej.id,
                numero=serie["numero"],
                repeticiones=serie["repeticiones"],
                peso=0.0  # peso inicial por defecto
            ))

    session.commit()

print("✅ Rutina 'Push Intermedio' creada correctamente con series peso 0.")
