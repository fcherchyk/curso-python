# Async en FastAPI

FastAPI es un framework **ASGI**: puede atender muchos requests a la vez en un solo hilo usando
`async`/`await`. Esto importa cuando tus endpoints **esperan** cosas lentas, como llamadas a otras
APIs, consultas a la base o lectura de archivos. Este capítulo te da lo justo de `asyncio` para
usarlo bien en la web (el módulo de concurrencia lo profundiza) y explica la regla más
importante: **cuándo usar `async def` y cuándo `def`**.

## El problema: esperar sin bloquear

Un endpoint que consulta tres APIs externas de 200 ms cada una, una tras otra, tarda 600 ms. Y
mientras espera la red, **el proceso no hace nada útil**. Con async, mientras una operación
espera, el *event loop* atiende otras: otros requests u otras llamadas del mismo request.

## `async def` y `await`

```python
import asyncio

async def buscar_precio(producto: str) -> float:
    await asyncio.sleep(0.2)          # simula la espera de la red
    return 100.0

async def main():
    precio = await buscar_precio("yerba")   # await: "esperá esto sin bloquear el loop"

asyncio.run(main())                   # punto de entrada desde código sincrónico
```

- Una función `async def` es una **corrutina**: llamarla **no la ejecuta**, devuelve un objeto que
  hay que esperar con `await` (como los generadores del módulo 03, que no corren hasta que se
  itera).
- `await` solo se puede usar dentro de `async def`.
- `asyncio.run(...)` arranca el loop. En FastAPI no hace falta: el servidor (uvicorn) ya lo tiene.

## Concurrencia: `asyncio.gather`

```python
async def cotizar(productos: list[str]) -> list[float]:
    return await asyncio.gather(*(buscar_precio(p) for p in productos))
```

`gather` lanza todas las corrutinas **a la vez** y espera a que terminen todas. Tres esperas de
200 ms tardan unos 200 ms en total, no 600. Devuelve los resultados **en el orden en que se
pasaron**.

Desde 3.11 también existe `asyncio.TaskGroup`, más seguro ante errores: si una tarea falla,
cancela las demás y levanta un `ExceptionGroup`, el del módulo 06.

### Timeouts

```python
try:
    async with asyncio.timeout(2):           # 3.11+
        datos = await consulta_lenta()
except TimeoutError:
    datos = None
```

En la web, **toda llamada externa debería tener un timeout**: si no, un servicio caído te deja
requests colgados para siempre.

## HTTP async: `httpx.AsyncClient`

`requests` es sincrónico. Para llamadas HTTP dentro de código async se usa **httpx**, que tiene
la misma API en sus dos versiones:

```python
import httpx

async with httpx.AsyncClient(base_url="https://api.precios.test", timeout=5) as cliente:
    r = await cliente.get("/precios/yerba")
    r.raise_for_status()                    # levanta si el status es 4xx/5xx
    precio = r.json()["precio"]
```

Reutilizá el cliente (en una dependencia o en el *lifespan* de la app): crear uno por request
desperdicia conexiones.

## La regla de oro en FastAPI: `async def` vs. `def`

```python
@app.get("/a")
async def a():                # corre EN el event loop
    datos = await cliente.get(...)      # ✓ esperas async
    return datos

@app.get("/b")
def b():                      # FastAPI lo corre en un THREAD POOL
    return requests.get(...).json()     # ✓ bloquea un thread, no el loop

@app.get("/c")
async def c():
    time.sleep(2)             # ✗✗ ¡bloquea el loop: la app ENTERA se congela 2 segundos!
    return requests.get(...)  # ✗✗ lo mismo
```

- Usá **`async def`** si adentro **solo** usás librerías async (`await httpx...`, drivers async).
- Usá **`def`** si usás librerías **sincrónicas** (SQLAlchemy sync, `requests`, cálculos). FastAPI
  las corre en un pool de threads, así no frenan al resto.
- **Nunca** llames a código bloqueante (`time.sleep`, `requests`, I/O de archivos pesado) dentro
  de un `async def`. Es el error más común con FastAPI. Si no tenés alternativa, usá
  `await asyncio.to_thread(funcion_bloqueante, ...)`.

Las dependencias siguen la misma regla: pueden ser `def` o `async def`.

## Tareas en segundo plano: `BackgroundTasks`

Para cosas que no tienen que demorar la respuesta (mandar un email, registrar una auditoría):

```python
from fastapi import BackgroundTasks

def enviar_confirmacion(email: str, pedido_id: int) -> None: ...

@app.post("/pedidos", status_code=201)
def crear(pedido: Pedido, tareas: BackgroundTasks):
    pedido_id = guardar(pedido)
    tareas.add_task(enviar_confirmacion, pedido.email, pedido_id)   # corre DESPUÉS de responder
    return {"id": pedido_id}
```

Son para tareas cortas. Si hace falta reintentar o procesar mucho, se usa una cola de verdad
(Celery, RQ, Arq).

## Testear código async

`TestClient` maneja los endpoints async solo, así que tus tests pueden ser sincrónicos. Para
probar funciones `async` sueltas, alcanza con `asyncio.run(...)` dentro del test (o con el plugin
`pytest-asyncio`). Para simular una API externa, `httpx.MockTransport`:

```python
async def manejador(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"precio": 100})

cliente = httpx.AsyncClient(transport=httpx.MockTransport(manejador), base_url="http://x")
```

## En los otros frameworks

- **Flask** es WSGI y sincrónico. Admite vistas `async def`, pero cada request ocupa un worker
  igual. Para mucha E/S concurrente, se escala con más procesos o threads.
- **Django** tiene vistas async y un ORM con métodos async (`aget`, `afilter`…) desde la versión
  4.x, aunque gran parte del ecosistema sigue siendo sincrónico.

## Resumen

- `async def` define una corrutina; `await` espera sin bloquear el loop; `asyncio.run` la arranca
  desde código sync.
- `asyncio.gather` para concurrencia (y `TaskGroup` en 3.11+); `asyncio.timeout` para cortar.
- `httpx.AsyncClient` para HTTP async; reutilizalo.
- En FastAPI: `async def` solo con librerías async; `def` con librerías sync; **nunca** bloquear
  dentro de `async def`.
- `BackgroundTasks` para tareas cortas después de responder.

## Ejercicio

Consultar precios a una API externa en paralelo (los tests verifican que **de verdad** sea
concurrente midiendo el tiempo), un timeout, un endpoint async con el cliente HTTP inyectado y
una tarea en segundo plano.

**Para profundizar:** [FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/),
[asyncio](https://docs.python.org/3/library/asyncio.html), [HTTPX Async](https://www.python-httpx.org/async/).
