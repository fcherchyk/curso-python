import asyncio
from collections.abc import AsyncIterator, Coroutine
from typing import Annotated, Any

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, Query
from pydantic import BaseModel

API_PRECIOS = "https://api.precios.test"
ENVIADOS: list[tuple[str, int]] = []
PEDIDOS: list[dict[str, Any]] = []


async def get_cliente() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url=API_PRECIOS, timeout=5) as cliente:
        yield cliente


def enviar_confirmacion(email: str, pedido_id: int) -> None:
    ENVIADOS.append((email, pedido_id))


class Pedido(BaseModel):
    email: str
    productos: list[str]


async def obtener_precio(cliente: httpx.AsyncClient, producto: str) -> float:
    r = await cliente.get(f"/precios/{producto}")
    r.raise_for_status()
    return float(r.json()["precio"])


async def precios_en_paralelo(
    cliente: httpx.AsyncClient, productos: list[str]
) -> dict[str, float]:
    precios = await asyncio.gather(*(obtener_precio(cliente, p) for p in productos))
    return dict(zip(productos, precios, strict=True))


async def con_timeout(corrutina: Coroutine[Any, Any, Any], segundos: float) -> Any:
    try:
        async with asyncio.timeout(segundos):
            return await corrutina
    except TimeoutError:
        return None


app = FastAPI()
Cliente = Annotated[httpx.AsyncClient, Depends(get_cliente)]


@app.get("/cotizacion")
async def cotizacion(cliente: Cliente, productos: Annotated[list[str], Query()]) -> dict[str, Any]:
    precios = await precios_en_paralelo(cliente, productos)
    return {"total": sum(precios.values()), "precios": precios}


@app.post("/pedidos", status_code=201)
def crear_pedido(pedido: Pedido, tareas: BackgroundTasks) -> dict[str, int]:
    pedido_id = len(PEDIDOS) + 1
    PEDIDOS.append({"id": pedido_id, **pedido.model_dump()})
    tareas.add_task(enviar_confirmacion, pedido.email, pedido_id)
    return {"id": pedido_id}
