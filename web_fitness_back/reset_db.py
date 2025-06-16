from sqlmodel import SQLModel, Session
from app.db import engine
from datetime import date
from sqlalchemy import text

def reset_database():
    print("⚠️ Reiniciando esquema de base de datos...")

    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()

    SQLModel.metadata.create_all(engine)
    print("✅ Esquema de base de datos reiniciado.")

if __name__ == "__main__":
    reset_database()
    