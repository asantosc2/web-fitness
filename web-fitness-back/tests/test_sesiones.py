import pytest
from .conftest import generar_email, crear_usuario, login_usuario

@pytest.mark.asyncio
async def test_sesion_desde_rutina_y_registro(async_client):
    email = generar_email()
    await crear_usuario(async_client, email)
    token = await login_usuario(async_client, email)
    headers = {"Authorization": f"Bearer {token}"}

    # Crear ejercicio y rutina
    ej = await async_client.post(
        "/ejercicios",
        json={"nombre": "Flexiones", "grupo_muscular": "Pecho", "tipo_equipo": "Peso corporal"},
        headers=headers,
    )
    ej_id = ej.json()["id"]

    resp = await async_client.post("/rutinas", json={"nombre": "Rutina diaria"}, headers=headers)
    rutina_id = resp.json()["id"]

    await async_client.post(
        f"/rutinas/{rutina_id}/ejercicios",
        json=[{"ejercicio_id": ej_id, "orden": 1, "series": 3, "repeticiones": 12}],
        headers=headers,
    )

    # Iniciar sesión
    resp = await async_client.post("/sesiones", json={"rutina_id": rutina_id}, headers=headers)
    assert resp.status_code == 200
    sesion = resp.json()

    # Ver ejercicios copiados
    resp = await async_client.get(f"/sesiones/{sesion['id']}/ejercicios", headers=headers)
    assert resp.status_code == 200
    ejercicios = resp.json()
    assert len(ejercicios) == 1
    ejercicio_id = ejercicios[0]["id"]

    # Registrar progreso
    resp = await async_client.put(
        f"/sesion-ejercicio/{ejercicio_id}",
        json={"peso": 20.0},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["peso"] == 20.0
