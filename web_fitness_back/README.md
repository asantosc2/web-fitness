# ⚙️ Backend – Plataforma Web Fitness

Este directorio contiene todo el código backend del proyecto **TFC: Plataforma Web Fitness**, 
desarrollado por **Alejandro Santos Cabrera** para el ciclo **Desarrollo de Aplicaciones Web (DAW)**.

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
* **httpx** – cliente HTTP para integración con OpenFoodFacts
* **Pytest** – pruebas automáticas para endpoints clave

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
│   ├── services/
│   │   └── openfood.py       # Cliente para OpenFoodFacts
│   └── routers/
│       ├── usuarios.py       # CRUD y auth de usuarios
│       ├── ejercicios.py     # CRUD de ejercicios con control de acceso
│       ├── rutinas.py        # Gestión de rutinas y ejercicios asociados
│       ├── sesiones.py       # Registro de sesiones de entrenamiento
│       ├── alimentos.py      # Gestión de alimentos + búsqueda externa
│       ├── progresos.py      # Seguimiento de peso y fotos
│       └── progreso_fotos.py # Subida/borrado de fotos de progreso
├── requirements.txt          # Dependencias del backend
├── docker-compose.yml        # Servicio PostgreSQL local
└── tests/                    # Pruebas automatizadas con pytest
```

---

## 🔐 Gestión de Usuarios

* Registro de usuarios con validaciones personalizadas.
* Inicio de sesión con autenticación basada en JWT.
* Recuperación de contraseña mediante token temporal.
* Actualización de perfil con verificación de seguridad.
* Eliminación de cuentas con control de roles (`is_admin`).
* Listado y consulta de usuarios (solo admins).

---

## 💪 Gestión de Ejercicios

* Creación de ejercicios propios.
* Visualización de ejercicios públicos y privados.
* Edición y eliminación con control de permisos.
* Filtros por grupo muscular, tipo de equipo, nivel, etc.

---

## 🧹 Gestión de Rutinas

* Crear rutinas personales o duplicar rutinas por defecto.
* Añadir ejercicios con orden, series, repeticiones, descanso.
* Editar y borrar rutinas completas.

---

## 🏋️ Registro de Sesiones de Entrenamiento

* Generación de una sesión a partir de una rutina.
* Registro real de entrenamiento (peso, reps, notas).
* Edición posterior de sesiones previas.

---

## 📈 Seguimiento de Progreso Físico

* Registro de peso corporal y comentarios por fecha.
* Subida de hasta 10 fotos por progreso (formato seguro).
* Visualización del histórico con fotos.
* Eliminación de fotos individuales o del progreso completo.

---

## 🍽️ Gestión de Alimentos (modo básico)

* Buscar alimentos reales en OpenFoodFacts (API externa).
* Guardar productos seleccionados como `Alimento` propio.
* Listar, editar y eliminar alimentos personalizados.

📌 **La creación de dietas completas (`Dieta`, `Comida`, `ComidaAlimento`) queda como futura implementación.**

---

## 🚀 Cómo levantar el backend localmente

```bash
cd web-fitness-back
python -m venv venv && source venv/bin/activate  # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d                             # Levanta PostgreSQL en localhost:5432
uvicorn app.main:app --reload                    # Servidor en http://localhost:8000
```

---

## 📌 Diagrama entidad-relación

```mermaid

    USUARIO ||--o{ RUTINA              : crea
    USUARIO ||--o{ PROGRESO            : registra
    USUARIO ||--o{ SESION              : realiza
    USUARIO ||--o{ ALIMENTO            : introduce
    RUTINA ||--o{ RUTINAEJERCICIO      : contiene
    EJERCICIO ||--o{ RUTINAEJERCICIO   : pertenece
    SESION ||--o{ SESIONEJERCICIO      : contiene
    EJERCICIO ||--o{ SESIONEJERCICIO   : ejecuta
    RUTINA ||--o{ SESION               : origen

    PROGRESO ||--o{ PROGRESOFOTO       : tiene
    ALIMENTO ||--o{ COMIDAALIMENTO     : está_en
    COMIDA ||--o{ COMIDAALIMENTO       : incluye
    DIETA ||--o{ COMIDA                : compone
    USUARIO ||--o{ DIETA               : define

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
    }

    PROGRESOFOTO {
        int id PK
        int progreso_id FK
        string ruta
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
```

---

## 🚧 Módulos pendientes

* 👨‍🍳 Implementación completa de dietas: `Dieta`, `Comida`, `ComidaAlimento`
* 🔍 Filtros y ordenaciones por campos en varios endpoints
* ⚠️ Control de errores más detallado (status, mensajes)
* ☁️ Despliegue completo en **Railway** con volúmenes y variables seguras

---

## 👤 Autor

**Alejandro Santos Cabrera**
TFC – Desarrollo de Aplicaciones Web (DAW)
Backend desarrollado con **FastAPI**, **PostgreSQL** y **Docker**
