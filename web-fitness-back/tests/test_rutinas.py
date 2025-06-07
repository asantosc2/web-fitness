import pytest
from .conftest import crear_usuario, login_usuario, generar_email

@pytest.mark.asyncio
async def test_crud_completo_rutina(async_client):
    email = generar_email()
    await crear_usuario(async_client, email)
    token = await login_usuario(async_client, email)
    headers = {"Authorization": f"Bearer {token}"}

    # Crear ejercicios base
    e1 = await async_client.post("/ejercicios", json={
        "nombre": "Press banca", "grupo_muscular": "Pecho", "tipo_equipo": "Barra"
    }, headers=headers)
    e2 = await async_client.post("/ejercicios", json={
        "nombre": "Curl bíceps", "grupo_muscular": "Brazos", "tipo_equipo": "Mancuernas"
    }, headers=headers)
    e1_id = e1.json()["id"]
    e2_id = e2.json()["id"]

    # Crear rutina
    r = await async_client.post("/rutinas", json={"nombre": "Upper A"}, headers=headers)
    assert r.status_code == 200
    rutina_id = r.json()["id"]

    # Agregar ejercicios
    ejercicios = [
        {"ejercicio_id": e1_id, "orden": 1, "series": 4, "repeticiones": 10},
        {"ejercicio_id": e2_id, "orden": 2, "series": 3, "repeticiones": 12}
    ]
    r = await async_client.post(f"/rutinas/{rutina_id}/ejercicios", json=ejercicios, headers=headers)
    assert r.status_code == 200
    asociaciones = r.json()
    assert len(asociaciones) == 2

    # Listar ejercicios de la rutina
    r = await async_client.get(f"/rutinas/{rutina_id}/ejercicios", headers=headers)
    assert r.status_code == 200
    lista = r.json()
    assert len(lista) == 2

    # Editar un ejercicio de la rutina (por ejemplo cambiar las repeticiones del segundo)
    id_asociacion = lista[1]["id"]
    r = await async_client.put(f"/rutina-ejercicio/{id_asociacion}", json={"repeticiones": 15}, headers=headers)
    assert r.status_code == 200
    assert r.json()["repeticiones"] == 15

    # Eliminar uno de los ejercicios
    r = await async_client.delete(f"/rutina-ejercicio/{id_asociacion}", headers=headers)
    assert r.status_code == 204

    # Verificar que queda solo uno
    r = await async_client.get(f"/rutinas/{rutina_id}/ejercicios", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1

    # Eliminar la rutina
    r = await async_client.delete(f"/rutinas/{rutina_id}", headers=headers)
    assert r.status_code == 204
    # Confirmar que la rutina ya no existe
    r = await async_client.get(f"/rutinas/{rutina_id}", headers=headers)
    assert r.status_code == 404