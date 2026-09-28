# pytest: fixtures, mocks y código testeable

Los tests de funciones puras son fáciles. El desafío aparece cuando el código **habla con el
mundo**: una API, una base de datos, el disco o el reloj. Este capítulo cubre las tres
herramientas para resolverlo: **fixtures** (preparar y limpiar), **dobles de prueba** (mocks
y fakes) y, la más importante, **diseñar el código para que sea testeable**.

## Fixtures: preparación reutilizable

Una fixture es una función que prepara algo para los tests. Los tests la piden **por nombre**,
como parámetro, y pytest la inyecta:

```python
import pytest

@pytest.fixture
def usuarios():
    return [{"id": 1, "nombre": "ana"}, {"id": 2, "nombre": "beto"}]

def test_cantidad(usuarios):          # pytest ve el parámetro y llama a la fixture
    assert len(usuarios) == 2
```

Cada test recibe una instancia **nueva** (con el scope por defecto, `function`), así que los
tests no se contaminan entre sí.

### Setup y teardown con `yield`

```python
@pytest.fixture
def conexion():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE t (x)")
    yield con                 # lo que recibe el test
    con.close()               # limpieza: corre aunque el test falle
```

### Scope y composición

```python
@pytest.fixture(scope="session")    # una vez para toda la corrida (caro de crear)
def motor_db(): ...

@pytest.fixture
def sesion(motor_db):               # las fixtures pueden pedir otras fixtures
    ...
```

Scopes: `function` (default), `class`, `module`, `package`, `session`.

### `conftest.py`

Las fixtures definidas en un `conftest.py` están disponibles para todos los tests de esa
carpeta y de sus subcarpetas, **sin importarlas**. Es el lugar para las fixtures compartidas.

### Fixtures incluidas que vas a usar siempre

| Fixture       | Para qué                                                        |
|---------------|-----------------------------------------------------------------|
| `tmp_path`    | un directorio temporal único (`Path`) para leer y escribir archivos |
| `capsys`      | capturar stdout/stderr: `capsys.readouterr().out`               |
| `monkeypatch` | reemplazar atributos, variables de entorno o dicts durante el test (y restaurarlos) |
| `caplog`      | capturar lo que se loguea                                       |

```python
def test_guarda_archivo(tmp_path):
    ruta = tmp_path / "reporte.txt"
    guardar(ruta, datos)
    assert ruta.read_text() == "..."

def test_lee_variable_de_entorno(monkeypatch):
    monkeypatch.setenv("API_KEY", "test")
    assert leer_config().api_key == "test"
```

## Diseñar para testear: inyección de dependencias

El código difícil de testear suele verse así:

```python
def temperatura(ciudad):
    r = httpx.get(f"https://api.clima.com/actual?ciudad={ciudad}")   # dependencia escondida
    return round(r.json()["temp_c"], 1)
```

Para testearlo hay que interceptar la red. En cambio, si la dependencia **se recibe**:

```python
class ClienteHTTP(Protocol):
    def get_json(self, url: str) -> dict: ...

def temperatura(ciudad: str, cliente: ClienteHTTP) -> float:
    datos = cliente.get_json(f"{BASE}/actual?ciudad={ciudad}")
    return round(datos["temp_c"], 1)
```

el test le pasa un **doble** y listo. Lo mismo vale para el reloj (`ahora: Callable[[], datetime]`),
el generador de ids o el repositorio de datos. Es la base de cómo FastAPI maneja las
dependencias (`Depends`), que vas a ver más adelante.

## Dobles de prueba: fakes y mocks

**Fake**: una implementación simple y real, en memoria.

```python
class ClienteFalso:
    def __init__(self, respuestas):
        self.respuestas = respuestas
        self.urls = []
    def get_json(self, url):
        self.urls.append(url)
        return self.respuestas[url]
```

**Mock**: un objeto que acepta cualquier llamada y **registra** cómo lo usaron. Viene en la
stdlib:

```python
from unittest.mock import Mock

cliente = Mock()
cliente.get_json.return_value = {"temp_c": 21.456}

assert temperatura("Rosario", cliente) == 21.5
cliente.get_json.assert_called_once_with(f"{BASE}/actual?ciudad=Rosario")
```

Lo esencial de `Mock`:

```python
m.metodo.return_value = 42                      # qué devuelve
m.metodo.side_effect = KeyError("x")            # que levante una excepción
m.metodo.side_effect = [1, 2, KeyError()]       # una respuesta distinta en cada llamada
m.metodo.side_effect = lambda url: {...}        # calcular la respuesta
m.metodo.assert_called_once_with(...)           # verificar la llamada
m.metodo.call_count, m.metodo.call_args_list
Mock(spec=ClienteHTTP)                          # solo acepta métodos que existen en el spec
```

### `patch`: cuando no podés inyectar

Si la dependencia está "cableada" adentro del código, `unittest.mock.patch` (o
`monkeypatch.setattr`) la reemplaza **temporalmente** en el módulo donde se **usa**:

```python
from unittest.mock import patch

with patch("app.servicio.httpx.get") as get:
    get.return_value.json.return_value = {"temp_c": 20}
    ...
```

La regla es parchear donde se busca el nombre, no donde se define. Usalo como último
recurso: si necesitás muchos `patch`, suele ser una señal de que conviene inyectar la
dependencia.

## No abuses de los mocks

- Mockeá **en los bordes** del sistema (red, disco, reloj, servicios externos), no tus
  propias clases internas.
- Si un test solo verifica que "se llamó a X con Y" y no ningún resultado, probablemente esté
  atado a la implementación y se rompa con cada refactor.
- Para una base de datos, muchas veces es mejor una **real** en memoria (SQLite) o en un
  contenedor que un mock.

## Resumen

- Fixtures: preparación por parámetro, `yield` para limpiar, `scope` para reutilizar y
  `conftest.py` para compartir.
- `tmp_path`, `capsys` y `monkeypatch` resuelven archivos, salida por consola y entorno.
- Inyectá las dependencias (con un Protocol como tipo) para poder pasar dobles.
- `Mock` con `return_value`/`side_effect` y `assert_called_once_with`; `patch` como último
  recurso.
- Mockeá los bordes, no tu propio código.

## Ejercicio

Escribís los tests para `clima.py` (el código está abajo). Requisitos: una **fixture** propia,
usar **`Mock`** y **`tmp_path`**. Como en el capítulo anterior, tus tests se corren contra el
original y contra **4 mutantes**.

```python
BASE = "https://api.clima.test/v1"

def temperatura(ciudad: str, cliente: ClienteHTTP) -> float:
    datos = cliente.get_json(f"{BASE}/actual?ciudad={ciudad}")
    return round(datos["temp_c"], 1)

def resumen(ciudades: Iterable[str], cliente: ClienteHTTP) -> dict[str, float]:
    """Temperatura de cada ciudad. Las que fallan con LookupError se omiten."""
    resultado = {}
    for ciudad in ciudades:
        try:
            resultado[ciudad] = temperatura(ciudad, cliente)
        except LookupError:
            continue
    return resultado

def guardar_reporte(ruta: Path, temperaturas: dict[str, float]) -> None:
    """Escribe "ciudad: temp" por línea, ordenado por ciudad."""
    lineas = [f"{c}: {t}" for c, t in sorted(temperaturas.items())]
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
```

**Para profundizar:** [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html),
[unittest.mock](https://docs.python.org/3/library/unittest.mock.html),
[monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html).
