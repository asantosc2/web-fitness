# ⚙️ Backend – Plataforma Web Fitness

Este directorio contiene todo el código backend del proyecto **TFC: Plataforma Web Fitness**, desarrollado por **Alejandro Santos Cabrera** para el ciclo **Desarrollo de Aplicaciones Web (DAW)**.

Está construido con **FastAPI + SQLModel + PostgreSQL**, e implementa una arquitectura moderna, escalable y bien documentada.

---

## 🧪 Tecnologías utilizadas

* **FastAPI** – framework web asíncrono y rápido
* **SQLModel** – ORM moderno (combinación de Pydantic + SQLAlchemy)
* **PostgreSQL** – base de datos relacional robusta (vía Docker)
* **Uvicorn** – servidor ASGI para desarrollo
* **JWT** – autenticación y autorización por token
* **Docker Compose** – entorno reproducible con contenedores
* **Pydantic** – validación de datos avanzada con `@field_validator`

---

## 📁 Estructura del proyecto

```bash
web-fitness-back/
├── README.md
├── app/
│   ├── main.py               # Punto de entrada de FastAPI
│   ├── db.py                 # Motor y sesión de base de datos
│   ├── models.py             # Modelos de datos (SQLModel)
│   ├── schemas.py            # Esquemas Pydantic para validaciones
│   ├── validators.py         # Validaciones personalizadas
│   ├── dependencies.py       # get_current_user + lógica de permisos
│   ├── auth.py               # Login, hash de contraseñas y tokens JWT
│   └── routers/
│       ├── usuarios.py       # CRUD y auth de usuarios
│       └── ejercicios.py     # CRUD de ejercicios con control de acceso
├── requirements.txt          # Dependencias del backend
└── docker-compose.yml        # Servicio PostgreSQL local
```

---

## 🔐 Módulo de Usuarios

* Registro con validaciones personalizadas
* Login y autenticación por JWT
* Acceso a `/usuarios`, `/login`, `/perfil`, `/recuperar`, `/restablecer`
* Permisos por rol (`is_admin`)
* Edición/borrado solo por el propio usuario (excepto admin)
* Recuperación de contraseña por token de un solo uso
* Protección de rutas con `Depends(get_current_user)`

---

## 💪 Módulo de Ejercicios

* Crear ejercicio (el usuario puede definir nombre, grupo, tipo)
* Si no es admin, no puede subir `imagen_url` ni `video_url`
* Ver ejercicios públicos (sin `usuario_id`) y los propios
* Editar y eliminar solo si es el dueño o administrador
* Los ejercicios públicos no se pueden eliminar
* Uso de filtros combinados `(usuario_id == None OR usuario_id == current_user.id)`

---

## 🚀 Cómo levantar el backend localmente

```bash
cd web-fitness-back
python -m venv venv && source venv/bin/activate  # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d                             # Levanta PostgreSQL en localhost:5432
uvicorn app.main:app --reload                    # Levanta el servidor en http://localhost:8000
```

## 📌 Diagrama entidad-relación

```mermaid
---
config:
  theme: base
---
erDiagram
    USUARIO ||--o{ RUTINA              : crea
    USUARIO ||--o{ PROGRESO            : registra
    USUARIO ||--o{ SESION              : realiza
    USUARIO ||--o{ DIETA               : define
    USUARIO ||--o{ ALIMENTO            : introduce
    RUTINA ||--o{ RUTINAEJERCICIO      : contiene
    EJERCICIO ||--o{ RUTINAEJERCICIO   : pertenece
    SESION ||--o{ SESIONEJERCICIO      : contiene
    EJERCICIO ||--o{ SESIONEJERCICIO   : ejecuta
    RUTINA ||--o{ SESION               : origen
    DIETA ||--o{ COMIDA                : contiene
    COMIDA ||--o{ COMIDAALIMENTO       : incluye
    COMIDAALIMENTO ||--|| ALIMENTO     : referencia

    USUARIO {
        int id PK
        string nombre
        string apellido
        string email
        string hashed_password
        date fecha_nacimiento
        datetime fecha_registro
        boolean is_admin
    }

    EJERCICIO {
        int id PK
        string nombre
        string grupo_muscular
        string tipo_equipo
        string imagen_url
        string video_url
    }

    RUTINA {
        int id PK
        string nombre
        string descripcion
        int usuario_id FK
        datetime fecha_creacion
        boolean es_defecto
    }

    RUTINAEJERCICIO {
        int id PK
        int rutina_id FK
        int ejercicio_id FK
        int orden
        int series
        int repeticiones
        int descanso
    }

    PROGRESO {
        int id PK
        int usuario_id FK
        date fecha
        float peso
        string comentarios
        string foto_url
    }

    SESION {
        int id PK
        int usuario_id FK
        date fecha
        int rutina_id FK
        string nota
    }

    SESIONEJERCICIO {
        int id PK
        int sesion_id FK
        int ejercicio_id FK
        int orden
        int series
        int repeticiones
        float peso
        string comentarios
    }

    DIETA {
        int id PK
        int usuario_id FK
        string nombre
        string descripcion
    }

    COMIDA {
        int id PK
        int dieta_id FK
        string nombre
    }

    COMIDAALIMENTO {
        int id PK
        int comida_id FK
        int alimento_id FK
        string porcion
        float calorias
        float proteinas
        float carbohidratos
        float grasas
    }

    ALIMENTO {
        int id PK
        string nombre
        float calorias_100g
        float proteinas_100g
        float carbohidratos_100g
        float grasas_100g
        float fibra_100g
        string imagen_url
        int usuario_id FK
    }
```

## 🚧 Módulos pendientes

* CRUD completo de rutinas (`Rutina`, `RutinaEjercicio`)
* Registro de sesiones de entrenamiento (`Sesion`, `SesionEjercicio`)
* Seguimiento físico con progreso y fotos (`Progreso`)
* Gestión de alimentos y dietas (`Dieta`, `Comida`, `Alimento`)
* Integración con API externa para búsqueda de alimentos (OpenFoodFacts)
* Tests automatizados con `pytest`
* Despliegue completo en Railway

---

## 👤 Autor

**Alejandro Santos Cabrera**
TFC – Desarrollo de Aplicaciones Web (DAW)
Backend desarrollado con **FastAPI** y **PostgreSQL**
