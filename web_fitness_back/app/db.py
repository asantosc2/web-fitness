from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()  # 👈 Necesario para que se lea el .env

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL no está definida. Revisa tu archivo .env")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
