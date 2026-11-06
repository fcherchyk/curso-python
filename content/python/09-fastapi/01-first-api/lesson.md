# FastAPI: tu primera API

FastAPI es el framework web de Python que más creció en los últimos años. Su idea central es
usar los **type hints** que ya escribís para todo: validar los datos de entrada, convertir tipos,
serializar las respuestas y generar la **documentación interactiva** (OpenAPI) automáticamente.
Está construido sobre **Starlette** (la parte web, ASGI) y **Pydantic** (la validación). Esta
misma app del curso está hecha con FastAPI.

## La app mínima

```python
from fastapi import FastAPI

app = FastAPI(title="Tienda")

@app.get("/")
def inicio():
    return {"mensaje": "Hola, FastAPI"}
```

```bash
uv add "fastapi[standard]"
uv run fastapi dev app.py       # http://127.0.0.1:8000  (o: uvicorn app:app --reload)
```

Abrí **`/docs`** y vas a ver la documentación interactiva (Swagger UI) generada a partir de tu
código, donde podés probar cada endpoint. En `/redoc` hay otra vista y en `/openapi.json`, el
esquema crudo.

## Parámetros de ruta: tipados

```python
@app.get("/productos/{id}")
def detalle(id: int):
    return {"id": id}
```

- La variable se declara en la ruta con llaves `{id}` y como **parámetro de la función**.
- El type hint **convierte y valida**: `/productos/7` llama con `id=7` (int), y `/productos/abc`
  responde **422** con un JSON que explica el error, sin llegar a tu función.

Comparalo con Flask, donde el converter va en la ruta (`<int:id>`) y los datos se leen de un
`request` global. En FastAPI, **todo lo que la función necesita está en su firma**.

## Query parameters: los parámetros que no están en la ruta

```python
@app.get("/productos")
def listar(q: str | None = None, pagina: int = 1, solo_stock: bool = False):
    ...
```

```
GET /productos?q=yerba&pagina=2&solo_stock=true
```

- Todo parámetro que **no** aparece en la ruta y es de tipo simple es un **query param**.
- Con default es opcional; sin default es **obligatorio** (si falta, 422).
- `bool` acepta `true/false/1/0/yes/no/on/off`.
- Para validar más, `Query`: `pagina: Annotated[int, Query(ge=1)] = 1` exige que sea ≥ 1.

## Respuestas y códigos de estado

```python
from fastapi import HTTPException, status

@app.get("/productos/{id}")
def detalle(id: int):
    producto = PRODUCTOS.get(id)
    if producto is None:
        raise HTTPException(status_code=404, detail="producto inexistente")
    return producto           # dict, lista o modelo Pydantic → JSON

@app.post("/productos", status_code=status.HTTP_201_CREATED)
def crear(...):
    ...
```

- Lo que devuelvas se serializa a JSON.
- `HTTPException` **se levanta** (no se devuelve) y FastAPI responde
  `{"detail": "..."}` con el código indicado.
- `status_code=` en el decorador define el código de éxito por defecto.

## El body: con Pydantic (adelanto)

Para recibir JSON en el body, se declara un **modelo**:

```python
from pydantic import BaseModel

class ProductoNuevo(BaseModel):
    nombre: str
    precio: int

@app.post("/productos", status_code=201)
def crear(datos: ProductoNuevo):        # un modelo como parámetro = el body
    ...
    return {"id": 3, **datos.model_dump()}
```

Si el JSON no tiene `nombre` o `precio` no es un número, FastAPI responde **422** detallando
cada campo inválido. Validar a mano, como en Flask, no hace falta. El próximo capítulo es
todo sobre Pydantic.

## `def` o `async def`

Las vistas pueden ser `def` o `async def`, y FastAPI acepta las dos. Por ahora usá `def`; en el
capítulo de async vemos cuándo conviene cada una.

## Testear con `TestClient`

```python
from fastapi.testclient import TestClient

cliente = TestClient(app)

def test_detalle():
    r = cliente.get("/productos/1")
    assert r.status_code == 200
    assert r.json()["nombre"] == "yerba"

def test_validacion():
    assert cliente.get("/productos/abc").status_code == 422
```

`TestClient` está basado en `httpx`: misma API (`get`, `post(json=...)`, `params=`,
`headers=`) y respuestas con `.json()`, `.text` y `.status_code`.

## Comparación con Flask

| Flask                                  | FastAPI                                     |
|----------------------------------------|---------------------------------------------|
| `@app.get("/p/<int:id>")`              | `@app.get("/p/{id}")` + `id: int`           |
| `request.args.get("q", type=int)`      | parámetro `q: int \| None = None`            |
| `request.get_json()` + validar a mano  | parámetro `datos: Modelo` (validación automática) |
| `return {...}, 404` o `abort(404)`     | `raise HTTPException(404, ...)`             |
| 400 hecho a mano                       | 422 automático con el detalle por campo     |
| sin documentación                      | `/docs` (OpenAPI) automático                |
| WSGI (sincrónico)                      | ASGI (sync y async)                         |

## Resumen

- `app = FastAPI()` y `@app.get/post/...` como en Flask.
- Parámetros de ruta `{id}` + `id: int`; el resto de los parámetros simples son query params.
- Los type hints validan y convierten: un dato inválido da 422 con el detalle.
- `raise HTTPException(status_code, detail)` para los errores; `status_code=` para el código
  de éxito.
- `/docs` gratis; `TestClient(app)` para testear.

## Ejercicio

La misma API de productos del primer capítulo de Flask, ahora en FastAPI: vas a ver cuánto
código de validación desaparece.

**Para profundizar:** [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/),
[Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/),
[Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/).
