# Flask: tu primera app

Flask es un **microframework**: trae lo mínimo para atender requests HTTP (ruteo, request y
response, plantillas) y deja todo lo demás (base de datos, formularios, auth) a extensiones
que elegís vos. Es simple, explícito y muy fácil de leer, y por eso sirve tanto para APIs chicas
como para entender qué hacen por dentro frameworks más grandes.

## La app mínima

```python
from flask import Flask

app = Flask(__name__)

@app.get("/")
def inicio():
    return "Hola, Flask!"
```

```bash
uv add flask
uv run flask --app app run --debug     # http://127.0.0.1:5000
```

- `Flask(__name__)` crea la aplicación. `__name__` le sirve para encontrar plantillas y archivos
  estáticos relativos al módulo.
- `@app.get("/")` registra la función como **vista** de esa ruta para el método GET. Es un
  decorador de registro, como los que viste en el módulo de funciones.
- Lo que devuelve la vista se convierte en la respuesta.
- `--debug` activa la recarga automática y el debugger en el navegador. **Nunca en
  producción**: permite ejecutar código.

## Rutas y métodos

```python
@app.get("/productos")                 # atajos: get, post, put, patch, delete
def listar(): ...

@app.post("/productos")
def crear(): ...

@app.route("/contacto", methods=["GET", "POST"])   # forma general
def contacto(): ...
```

### Variables de ruta y converters

```python
@app.get("/usuarios/<nombre>")             # string (sin "/")
def perfil(nombre): ...

@app.get("/productos/<int:id>")            # convierte a int; si no es número → 404
def detalle(id): ...

@app.get("/archivos/<path:ruta>")          # acepta "/" adentro
def archivo(ruta): ...
```

Converters: `string` (por defecto), `int`, `float`, `path` y `uuid`. Si el valor no matchea,
Flask responde **404** sin llegar a tu función.

## El request: `flask.request`

```python
from flask import request

@app.get("/buscar")
def buscar():
    q = request.args.get("q", "")               # query string ?q=...
    pagina = request.args.get("pagina", 1, type=int)
    ...

@app.post("/productos")
def crear():
    datos = request.get_json(silent=True)        # body JSON (None si no es JSON válido)
    nombre = request.form.get("nombre")          # body de un formulario
    token = request.headers.get("Authorization")
    ...
```

`request` es un objeto **global por request**: Flask usa variables de contexto (*context
locals*) para que cada request vea el suyo, aunque haya varios en paralelo. Es cómodo, pero
"mágico". FastAPI, en cambio, te pasa los datos como parámetros de la función.

`request.args.get(..., type=int)` devuelve el default si la conversión falla, en lugar de
levantar una excepción.

## La respuesta

Una vista puede devolver:

```python
return "texto"                                  # 200, text/html
return {"id": 1, "nombre": "yerba"}             # un dict → JSON automáticamente
return jsonify([1, 2, 3])                       # JSON explícito (sirve para listas)
return {"error": "no existe"}, 404              # (cuerpo, status)
return {"id": 7}, 201, {"Location": "/productos/7"}   # (cuerpo, status, headers)
return redirect(url_for("listar"))              # 302
abort(404)                                      # corta la vista con un error HTTP
```

Los códigos de estado importan: **200** OK, **201** creado, **204** sin contenido, **400**
request inválido, **401** sin autenticar, **403** sin permiso, **404** no existe, **422**
datos inválidos y **500** error del servidor.

## Testear con `test_client`

Flask trae un cliente que hace requests **sin levantar un servidor**:

```python
def test_crear():
    cliente = app.test_client()
    r = cliente.post("/productos", json={"nombre": "yerba", "precio": 3500})
    assert r.status_code == 201
    assert r.get_json()["nombre"] == "yerba"

    r = cliente.get("/buscar", query_string={"q": "yer"})
    assert r.status_code == 200
```

`r.get_json()` parsea el cuerpo y `r.text` lo da como string. Es la forma estándar de testear
apps Flask, y la que usan los tests de este módulo.

## Comparación rápida de los tres frameworks

| Concepto          | Flask                        | FastAPI                         | Django                      |
|-------------------|------------------------------|---------------------------------|-----------------------------|
| Ruta              | `@app.get("/x/<int:id>")`    | `@app.get("/x/{id}")` + `id: int` | `path("x/<int:id>/", vista)` |
| Datos del request | `request` global             | parámetros con type hints        | `request` como argumento    |
| JSON              | devolver un dict             | devolver un dict o un modelo     | `JsonResponse(...)`          |
| Validación        | manual o con extensiones     | automática (Pydantic)            | Forms / serializers         |
| Filosofía         | mínimo, elegís las piezas    | APIs modernas y tipadas          | baterías incluidas          |

## Resumen

- `app = Flask(__name__)` y vistas registradas con `@app.get`/`@app.post`.
- Variables de ruta con converters (`<int:id>`); si no matchea, 404.
- `request.args`, `request.get_json()`, `request.form` y `request.headers`.
- Devolver un dict da JSON; `(cuerpo, status)` para elegir el código; `abort()` para cortar.
- `app.test_client()` para testear sin servidor.

## Ejercicio

Una API chica de productos en memoria: texto, ruta con variable, query string con validación,
detalle con 404 y alta con 201.

**Para profundizar:** [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/),
[Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/).
