"""Reto S4 — la colección Postman del reto S3 (/users) convertida a Python puro.

Cada test replica un request de RETO_S3_Marcelo_Ancieta.postman_collection.json
con las mismas validaciones, ahora sobre la fixture `api` y asserts de pytest.
Reutiliza `cumple_contrato` de test_posts_crud (DRY) con el contrato de user.

Bonus: los payloads del POST viven en data/users_payloads.json — agregar un
caso nuevo = agregar una entrada al JSON. Cero código nuevo.
"""

import time

import pytest

from conftest import load_json
from test_posts_crud import cumple_contrato

# Contrato del recurso user: campo -> tipo esperado (el JSON Schema de la S3, versión KISS)
CONTRATO_USER = {"id": int, "name": str, "username": str, "email": str}

CASOS_USER = load_json("users_payloads.json")


def test_listar_users(api):
    respuesta = api.get("/users")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 10
    assert respuesta.elapsed.total_seconds() < 2.0


def test_detalle_cumple_contrato(api):
    respuesta = api.get("/users/1")

    assert respuesta.status_code == 200
    usuario = respuesta.json()
    assert cumple_contrato(usuario, CONTRATO_USER)
    assert usuario["id"] == 1


def test_crear_user(api):
    # Nombre único por corrida — igual que el pre-request script de Postman
    nombre = f"User_{time.time_ns()}"
    payload = {"name": nombre, "username": "mancieta", "email": "marcelo.ancieta@example.com"}

    respuesta = api.post("/users", json=payload)

    assert respuesta.status_code == 201
    assert respuesta.json()["name"] == nombre


def test_actualizar_user(api):
    payload = {"id": 1, "name": "Marcelo Ancieta", "username": "mancieta", "email": "mancieta@example.com"}

    respuesta = api.put("/users/1", json=payload)

    assert respuesta.status_code == 200
    actualizado = respuesta.json()
    for campo, valor in payload.items():
        assert actualizado[campo] == valor


def test_eliminar_user(api):
    respuesta = api.delete("/users/1")

    assert respuesta.status_code == 200
    assert respuesta.json() == {}


def test_user_inexistente_devuelve_404(api):
    respuesta = api.get("/users/999999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {}


# ── Bonus: creación de users con datos externos (data-driven) ─────────────────

@pytest.mark.parametrize(
    "caso",
    CASOS_USER,
    ids=[c["caso"] for c in CASOS_USER],
)
def test_crear_user_con_datos_externos(api, caso):
    respuesta = api.post("/users", json=caso["payload"])

    assert respuesta.status_code == 201
    creado = respuesta.json()
    # La API hace eco del payload: cada campo enviado debe volver igual
    for campo, valor in caso["payload"].items():
        assert creado[campo] == valor
