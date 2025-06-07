#main.py
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db import engine
from app.routers import usuarios, ejercicios, rutinas, sesiones, alimentos, progresos, progreso_fotos

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    print("Base de datos inicializada correctamente.")

app.include_router(usuarios.router)
app.include_router(ejercicios.router)
app.include_router(rutinas.router)
app.include_router(sesiones.router)
app.include_router(alimentos.router)
app.include_router(progresos.router)
app.include_router(progreso_fotos.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de mi aplicación de fitness"}

