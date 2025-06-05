from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db import engine
from app.routers import usuarios

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    print("Base de datos inicializada correctamente.")

app.include_router(usuarios.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de mi aplicación de fitness"}

