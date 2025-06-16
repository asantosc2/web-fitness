import pytest
from .conftest import generar_email, crear_usuario, login_usuario

@pytest.mark.asyncio
async def test_usuario_login(async_client):
    email = generar_email()
    await crear_usuario(async_client, email)
    response = await async_client.post("/login", json={"email": email, "password": "Testpass123@"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

@pytest.mark.asyncio
async def test_usuario_update(async_client):
    email = generar_email()
    usuario = await crear_usuario(async_client, email)
    token = await login_usuario(async_client, email)
    headers = {"Authorization": f"Bearer {token}"}
    new_name = "Nuevo"
    response = await async_client.put(f"/usuarios/{usuario['id']}", json={"nombre": new_name}, headers=headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == new_name

@pytest.mark.asyncio
async def test_usuario_get(async_client):
    email = generar_email()
    usuario = await crear_usuario(async_client, email)
    token = await login_usuario(async_client, email)
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get(f"/usuarios/{usuario['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == email

@pytest.mark.asyncio
async def test_usuario_delete(async_client):
    email = generar_email()
    usuario = await crear_usuario(async_client, email)
    token = await login_usuario(async_client, email)
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.delete(f"/usuarios/{usuario['id']}", headers=headers)
    assert response.status_code in {200, 204}
    # Confirm deletion
    response = await async_client.get(f"/usuarios/{usuario['id']}", headers=headers)
    assert response.status_code == 404