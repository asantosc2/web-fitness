from fastapi import FastAPI
from app.models import SQLModel
from app.db import engine

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de mi aplicación de fitness"}

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    print("Base de datos inicializada correctamente.")