import uuid
import pytest_asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client

async def crear_usuario(client, email, password="Testpass123@", is_admin=False):
    data = {
        "nombre": "Test",
        "apellido": "User",
        "email": email,
        "password": password,
        "fecha_nacimiento": "1990-01-01"
    }
    resp = await client.post("/usuarios", json=data)
    resp.raise_for_status()

    # Si hay que convertir a admin, hacer login y modificar el campo
    if is_admin:
        token = await login_usuario(client, email, password)
        headers = {"Authorization": f"Bearer {token}"}
        resp_admin = await client.put(
            f"/usuarios/{resp.json()['id']}",
            json={"is_admin": True},
            headers=headers
        )
        resp_admin.raise_for_status()
        return resp_admin.json()

    return resp.json()

async def login_usuario(client, email, password="Testpass123@"):
    resp = await client.post("/login", json={"email": email, "password": password})
    resp.raise_for_status()
    return resp.json()["access_token"]

def generar_email():
    return f"test_{uuid.uuid4()}@example.com"