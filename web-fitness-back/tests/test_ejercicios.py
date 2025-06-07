import pytest
from tests.conftest import generar_email, crear_usuario, login_usuario

EJERCICIO_DATA = {
    "nombre": "Press Banca",
    "grupo_muscular": "Pecho",
    "tipo_equipo": "Barra"
}

@pytest.mark.asyncio
async def test_crear_listar_borrar_ejercicio(async_client):
    email = generar_email()
    await crear_usuario(async_client, email)
    token = await login_usuario(async_client, email)
    headers = {"Authorization": f"Bearer {token}"}

    # Crear
    resp = await async_client.post("/ejercicios", json=EJERCICIO_DATA, headers=headers)
    assert resp.status_code == 200
    ejercicio = resp.json()

    # Listar
    resp = await async_client.get("/ejercicios", headers=headers)
    assert resp.status_code == 200
    ids = [e["id"] for e in resp.json()]
    assert ejercicio["id"] in ids

    # Obtener individual
    resp = await async_client.get(f"/ejercicios/{ejercicio['id']}", headers=headers)
    assert resp.status_code == 200

    # Borrar
    resp = await async_client.delete(f"/ejercicios/{ejercicio['id']}", headers=headers)
    assert resp.status_code in {200, 204}

@pytest.mark.asyncio
async def test_listar_ejercicios_admin(async_client):
    email = generar_email()
    # Crear un usuario admin manualmente
    await crear_usuario(async_client, email, password="Test123!", is_admin=True)
    token = await login_usuario(async_client, email, password="Test123!")
    headers = {"Authorization": f"Bearer {token}"}

    # Crear ejercicios para asegurar que hay algo en la lista
    await async_client.post("/ejercicios", json={
        "nombre": "Dominadas",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Barra",
        "descripcion": "Ejercicio de tracción"
    }, headers=headers)

    response = await async_client.get("/ejercicios", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
