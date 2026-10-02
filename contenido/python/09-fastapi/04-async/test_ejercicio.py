import asyncio
import time

import ejercicio
import httpx
import pytest
from ejercicio import (
    app,
    con_timeout,
    get_cliente,
    obtener_precio,
    precios_en_paralelo,
)
from fastapi.testclient import TestClient

PRECIOS = {"yerba": 3500.0, "cafe": 9800.0, "te": 1200.0, "azucar": 900.0, "leche": 1500.0}
DEMORA = 0.2


async def api_falsa(request: httpx.Request) -> httpx.Response:
    await asyncio.sleep(DEMORA)  # cada consulta "tarda" 200 ms
    producto = request.url.path.rsplit("/", 1)[-1]
    if producto not in PRECIOS:
        return httpx.Response(404, json={"error": "no existe"})
    return httpx.Response(200, json={"precio": PRECIOS[producto]})


def cliente_falso() -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(api_falsa), base_url="http://falsa")


def test_obtener_precio():
    async def caso():
        async with cliente_falso() as c:
            return await obtener_precio(c, "yerba")

    assert asyncio.run(caso()) == 3500.0


def test_precios_en_paralelo_es_concurrente():
    async def caso():
        async with cliente_falso() as c:
            inicio = time.perf_counter()
            res = await precios_en_paralelo(c, list(PRECIOS))
            return res, time.perf_counter() - inicio

    res, demora = asyncio.run(caso())
    assert res == PRECIOS
    assert demora < DEMORA * 2.5, f"tardó {demora:.2f}s: ¿las consultas van una por una?"


def test_con_timeout():
    async def lenta():
        await asyncio.sleep(1)
        return "tarde"

    async def rapida():
        return "ok"

    assert asyncio.run(con_timeout(rapida(), 0.5)) == "ok"
    inicio = time.perf_counter()
    assert asyncio.run(con_timeout(lenta(), 0.1)) is None
    assert time.perf_counter() - inicio < 0.5


@pytest.fixture
def cliente():
    async def override():
        async with cliente_falso() as c:
            yield c

    app.dependency_overrides[get_cliente] = override
    ejercicio.ENVIADOS.clear()
    ejercicio.PEDIDOS.clear()
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_endpoint_cotizacion(cliente):
    inicio = time.perf_counter()
    r = cliente.get("/cotizacion", params={"productos": ["yerba", "cafe", "te"]})
    assert r.status_code == 200
    assert r.json() == {
        "total": 14500.0,
        "precios": {"yerba": 3500.0, "cafe": 9800.0, "te": 1200.0},
    }
    assert time.perf_counter() - inicio < DEMORA * 2.5, "el endpoint también tiene que ser concurrente"


def test_pedido_con_tarea_en_segundo_plano(cliente):
    r = cliente.post("/pedidos", json={"email": "ana@x.com", "productos": ["yerba"]})
    assert r.status_code == 201
    assert r.json() == {"id": 1}
    assert ejercicio.ENVIADOS == [("ana@x.com", 1)]
