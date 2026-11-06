# Inyección de dependencias con `Depends`

La función más poderosa de FastAPI es su sistema de **dependencias**. Una dependencia es una
función que FastAPI ejecuta **antes** de tu endpoint para darle algo que necesita: el usuario
autenticado, una sesión de base de datos, la configuración o los parámetros de paginación.
Resuelve con una sola idea lo que en Flask necesitaba decoradores, `g` y `current_app`, y hace
que todo sea **fácil de reemplazar en los tests**.

## Lo básico

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Query

def paginacion(
    pagina: Annotated[int, Query(ge=1)] = 1,
    por_pagina: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, int]:
    return {"offset": (pagina - 1) * por_pagina, "limite": por_pagina}

@app.get("/productos")
def listar(pag: Annotated[dict[str, int], Depends(paginacion)]):
    return PRODUCTOS[pag["offset"] : pag["offset"] + pag["limite"]]
```

- `Depends(funcion)` le dice a FastAPI: "antes de llamar al endpoint, llamá a `funcion` y pasame
  lo que devuelve".
- La dependencia **declara sus propios parámetros** (query, headers, otras dependencias) y
  FastAPI los resuelve igual que los de un endpoint. Aparecen en `/docs`.
- `Annotated[T, Depends(f)]` es la forma recomendada. También se puede definir un alias,
  `Paginacion = Annotated[dict, Depends(paginacion)]`, y usarlo en muchos endpoints.

## Autenticación como dependencia

```python
from fastapi import Header, HTTPException, status

def usuario_actual(authorization: Annotated[str | None, Header()] = None) -> Usuario:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="falta el token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    usuario = buscar_por_token(authorization.removeprefix("Bearer "))
    if usuario is None:
        raise HTTPException(401, detail="token inválido")
    return usuario

@app.get("/yo")
def yo(usuario: Annotated[Usuario, Depends(usuario_actual)]):
    return usuario
```

- `Header()` lee un header. El nombre del parámetro se convierte: `authorization` →
  `Authorization`, `x_token` → `X-Token`.
- Si la dependencia **levanta** `HTTPException`, el endpoint ni se ejecuta.
- FastAPI trae utilidades como `OAuth2PasswordBearer` y `HTTPBearer`, que además integran el
  botón "Authorize" en `/docs`.

## Subdependencias: componer

Las dependencias pueden depender de otras, y así se arma una cadena:

```python
def solo_admin(usuario: Annotated[Usuario, Depends(usuario_actual)]) -> Usuario:
    if not usuario.es_admin:
        raise HTTPException(403, "requiere permisos de administrador")
    return usuario

@app.delete("/productos/{id}", status_code=204)
def borrar(id: int, admin: Annotated[Usuario, Depends(solo_admin)]): ...
```

FastAPI arma el grafo y **cachea cada dependencia dentro del mismo request**: si dos
dependencias piden `usuario_actual`, se ejecuta una sola vez.

Si no necesitás el valor, la dependencia puede ir en el decorador:
`@app.delete(..., dependencies=[Depends(solo_admin)])`. También en un router entero.

## Dependencias con `yield`: setup y limpieza

```python
def get_session():
    session = SessionLocal()
    try:
        yield session            # el endpoint usa la sesión
    finally:
        session.close()          # corre después de enviar la respuesta
```

Es el mismo patrón de los context managers del módulo 04. Así se maneja la sesión de base de
datos en el capítulo de SQLAlchemy.

## Inyectar servicios y configuración

```python
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:          # se crea una sola vez
    return Settings()

def get_repo() -> RepositorioProductos:
    return RepositorioSQL(...)

@app.get("/productos")
def listar(repo: Annotated[RepositorioProductos, Depends(get_repo)]):
    return repo.listar()
```

El endpoint no sabe **de dónde** sale el repositorio: solo declara que lo necesita. Esa es la
inversión de dependencias del módulo de testing, ahora integrada en el framework.

## Tests: `dependency_overrides`

La gran ventaja: en los tests reemplazás cualquier dependencia sin parchear nada.

```python
def repo_falso():
    return RepositorioEnMemoria([...])

def test_listar():
    app.dependency_overrides[get_repo] = repo_falso
    app.dependency_overrides[usuario_actual] = lambda: Usuario(nombre="test", es_admin=True)
    try:
        r = TestClient(app).get("/productos")
        ...
    finally:
        app.dependency_overrides.clear()
```

La clave del dict es la **función original** y el valor, la que la reemplaza.

## Comparación

| Necesidad              | Flask                          | FastAPI                                  |
|------------------------|--------------------------------|------------------------------------------|
| usuario autenticado    | decorador + `g.usuario`        | `Depends(usuario_actual)`                |
| configuración          | `current_app.config`           | `Depends(get_settings)`                  |
| sesión de base         | `db.session` (scoped)          | `Depends(get_session)` con `yield`       |
| reemplazar en tests    | config de la factory o mocks   | `app.dependency_overrides`               |
| permisos compuestos    | decoradores apilados           | subdependencias                           |

## Resumen

- `Depends(f)`: FastAPI llama a `f` (resolviendo sus parámetros) y le pasa el resultado al endpoint.
- Autenticación, paginación, configuración y repositorios como dependencias.
- Las subdependencias se componen y se cachean dentro de cada request.
- `yield` para el setup y la limpieza (sesiones).
- `app.dependency_overrides[original] = falsa` para testear.

## Ejercicio

Paginación, autenticación por token, un permiso de admin compuesto y un repositorio
inyectado que los tests reemplazan con `dependency_overrides`.

**Para profundizar:** [FastAPI: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/),
[Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
