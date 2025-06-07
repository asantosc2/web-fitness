import uuid
import pytest
import pytest_asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client

def generar_email():
    return f"test_{uuid.uuid4()}@example.com"

async def crear_usuario(client, email, password="Testpass123@"):
    data = {
        "nombre": "Test",
        "apellido": "User",
        "email": email,
        "password": password,
        "fecha_nacimiento": "1990-01-01"
    }
    resp = await client.post("/usuarios", json=data)
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    return resp.json()

async def login_usuario(client, email, password="Testpass123@"):
    resp = await client.post("/login", json={"email": email, "password": password})
    resp.raise_for_status()
    return resp.json()["access_token"]