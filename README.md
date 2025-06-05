# 🏋️ Plataforma Web Fitness (TFC – Alejandro Santos)

Proyecto de fin de ciclo DAW: una aplicación web para la gestión personalizada de entrenamientos, dietas y progreso físico.

---

## 🧠 Tecnologías utilizadas

* **Frontend**: React.js + Tailwind CSS
* **Backend**: FastAPI + SQLModel + Uvicorn
* **Base de datos**: PostgreSQL (Docker)
* **Contenedores**: Docker & Docker Compose
* **Control de versiones**: Git + GitHub
* **Prototipos y diseño**: Figma
* **Despliegue**: Railway (backend) + Vercel (frontend)

---

## 📊 Funcionalidades implementadas

### 🧐 Usuario

* Registro de usuario
* Login con autenticación JWT
* Recuperación de contraseña por correo (token temporal)
* Registro automático de fecha de alta
* Actualización de perfil
* Eliminación de cuenta (solo administradores pueden eliminar cuentas ajenas)

### 💪 Ejercicios

* Ver todos los ejercicios predefinidos
* Crear ejercicios personalizados por usuario
* Filtros por grupo muscular, equipo, tipo, etc.

### 🧩 Rutinas

* Crear rutinas con nombre y descripción
* Añadir ejercicios a la rutina con orden, series, repeticiones y descanso
* Ver rutinas propias y rutinas por defecto
* Copiar rutinas por defecto a la cuenta del usuario

### 🔁 Sesiones de entrenamiento

* Iniciar sesión desde rutina (copia ejercicios)
* Registrar peso real, repeticiones efectivas, comentarios
* Consultar sesiones pasadas y ver historial

### 📈 Progreso físico

* Registrar peso corporal, comentarios y fotos
* Consultar evolución semanal o mensual

### 🥽 Consulta nutricional

* Buscar alimentos reales por nombre en la API Open Food Facts
* Mostrar nombre, marca, calorías y macros por 100g
* Mostrar imagen del alimento para verificación visual

### 🍽️ Dietas y comidas

* Crear dietas personales
* Dividirlas en comidas (desayuno, comida, cena...)
* Añadir alimentos por porción con macros personalizados
* Usar alimentos de Open Food Facts o creados por el usuario

### ✍️ Crear alimentos personalizados

* El usuario puede crear sus propios alimentos (ej: "batido postentreno")
* Introducir nombre, imagen opcional, macros por 100g
* Asociados únicamente al usuario que los crea

---

## 📆 Estructura del proyecto

```bash
web-fitness/
├── web-fitness-front/     # React + Tailwind
├── web-fitness-back/      # FastAPI + SQLModel
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   │   └── usuarios.py
│   │   ├── db.py
│   │   ├── auth.py
│   │   ├── dependencies.py
│   │   ├── schemas.py
│   │   ├── validators.py
│   ├── requirements.txt
│   └── docker-compose.yml
└── entregas/              # Informes, entregables
```

---

## 🚪 Cómo ejecutar el backend

```bash
cd web-fitness-back
python -m venv venv && source venv/bin/activate  # o .\venv\Scripts\activate en Windows
pip install -r requirements.txt
docker compose up -d  # levanta PostgreSQL
uvicorn app.main:app --reload  # arranca la API
```

---

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
