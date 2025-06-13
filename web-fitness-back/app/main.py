#main.py
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db import engine
from app.routers import usuarios, ejercicios, rutinas, sesiones, alimentos, progresos, progreso_fotos
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
security = HTTPBearer()


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



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI - Plataforma Web Fitness",
        version="1.0.0",
        description="Documentación del backend de Alejandro Santos Cabrera",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de mi aplicación de fitness"}

# Habilitar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
