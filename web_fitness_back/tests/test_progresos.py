import pytest
from httpx import AsyncClient
from .conftest import generar_email, crear_usuario, login_usuario
from datetime import date
import os

CARPETA_FOTOS = "progreso_fotos"

@pytest.mark.asyncio
async def test_progreso_completo(async_client: AsyncClient):
    # 1. Crear usuario y loguearse
    email = generar_email()
    await crear_usuario(async_client, email)
    token = await login_usuario(async_client, email)
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear progreso
    data = {
        "fecha": str(date.today()),
        "peso": 78.5,
        "comentarios": "Inicio del corte"
    }
    res = await async_client.post("/progresos", json=data, headers=headers)
    assert res.status_code == 200
    progreso = res.json()
    progreso_id = progreso["id"]

    # 3. Subir 2 fotos
    files = [
        ("archivos", ("frontal.jpg", open("tests/testsfiles/frontal.jpg", "rb"), "image/jpeg")),
        ("archivos", ("back.jpg", open("tests/testsfiles/back.jpg", "rb"), "image/jpeg")),
    ]
    res = await async_client.post(f"/progresos/{progreso_id}/fotos", files=files, headers=headers)
    assert res.status_code == 200
    fotos = res.json()
    assert len(fotos) == 2

    foto_id_a_eliminar = fotos[0]["id"]
    nombre_archivo = fotos[0]["ruta"]
    ruta_archivo = os.path.join(CARPETA_FOTOS, nombre_archivo)
    assert os.path.exists(ruta_archivo)

    # 4. Eliminar una foto
    res = await async_client.delete(f"/progresos/fotos/{foto_id_a_eliminar}", headers=headers)
    assert res.status_code == 204
    assert not os.path.exists(ruta_archivo)

    # 5. Verificar que solo queda una foto
    res = await async_client.get(f"/progresos/{progreso_id}", headers=headers)
    assert res.status_code == 200
    progreso_actualizado = res.json()
    assert len(progreso_actualizado["fotos"]) == 1
    ids_restantes = [f["id"] for f in progreso_actualizado["fotos"]]
    assert foto_id_a_eliminar not in ids_restantes

    # 6. Eliminar progreso
    res = await async_client.delete(f"/progresos/{progreso_id}", headers=headers)
    assert res.status_code == 204
