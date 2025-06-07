#test_alimentos.py
import pytest
from .conftest import generar_email, crear_usuario, login_usuario
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_buscar_y_guardar_alimento(async_client: AsyncClient):
    # Registro y login de usuario
    email = generar_email()
    await crear_usuario(async_client, email)
    token = await login_usuario(async_client, email)
    headers = {"Authorization": f"Bearer {token}"}

    # Buscar alimento en OpenFood
    r = await async_client.get("/alimentos/buscar-openfood", params={"query": "pollo"})
    assert r.status_code == 200
    productos = r.json()
    assert isinstance(productos, list)
    assert len(productos) > 0

    # Guardar el primer producto como alimento propio
    primero = productos[0]
    alimento_data = {
        "nombre": primero["nombre"],
        "calorias_100g": primero["kcal"],
        "proteinas_100g": primero["proteinas"],
        "carbohidratos_100g": primero["carbohidratos"],
        "grasas_100g": primero["grasas"],
        "imagen_url": primero.get("imagen_url")
    }

    r = await async_client.post("/alimentos/desde-openfood", json=alimento_data, headers=headers)
    assert r.status_code == 200
    alimento = r.json()
    assert alimento["nombre"] == alimento_data["nombre"]

    # Verificar que aparece en la lista de alimentos propios
    r = await async_client.get("/alimentos", headers=headers)
    assert r.status_code == 200
    alimentos = r.json()
    assert any(a["id"] == alimento["id"] for a in alimentos)

    # Eliminarlo
    r = await async_client.delete(f"/alimentos/{alimento['id']}", headers=headers)
    assert r.status_code == 204
