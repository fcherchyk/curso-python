# Módulos, paquetes e imports

Cada archivo `.py` es un **módulo**, y una carpeta con módulos es un **paquete**. Entender
cómo Python encuentra y ejecuta lo que importás evita los errores más frustrantes del día a
día, como `ModuleNotFoundError`, imports circulares o código que se ejecuta "solo" al
importar.

## Qué pasa cuando hacés `import x`

1. Python busca `x` en `sys.modules`, el caché de módulos ya importados. Si está, lo reutiliza.
2. Si no está, lo busca en los directorios de `sys.path`: primero el directorio del script
   que ejecutaste (o el actual), después `PYTHONPATH` y al final la stdlib y `site-packages`.
3. Lo encuentra y **ejecuta el archivo completo, de arriba a abajo**, una sola vez.
4. Guarda el objeto módulo en `sys.modules` y lo asigna al nombre `x`.

El punto 3 es clave: **importar ejecuta código**. Por eso un módulo no debería hacer trabajo
pesado ni tener efectos secundarios (conectarse a una base, imprimir, leer archivos) en el
nivel superior.

## Formas de importar

```python
import json                        # usás json.loads(...)
import numpy as np                 # alias (convención de la comunidad)
from pathlib import Path           # traés un nombre concreto
from os import path as osp
from collections import Counter, defaultdict
```

- `import modulo` deja claro de dónde viene cada cosa (`json.loads`).
- `from modulo import nombre` es cómodo para nombres muy usados y sin ambigüedad (`Path`).
- **Evitá `from modulo import *`**: ensucia el namespace, esconde de dónde vienen los nombres
  y confunde a las herramientas.

Orden convencional (ruff lo ordena solo con la regla `I`): stdlib, después terceros y al
final tu proyecto, en bloques separados por una línea en blanco.

## `if __name__ == "__main__":`

Cada módulo tiene la variable `__name__`. Vale el nombre del módulo cuando se **importa**
(`"utiles"`) y `"__main__"` cuando se **ejecuta** directamente (`python utiles.py`):

```python
# utiles.py
def main(argv: list[str]) -> int:
    print("procesando", argv)
    return 0

if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
```

Así el archivo sirve como librería (se importa sin efectos) y como script. Tener una función
`main(argv) -> int` en lugar de código suelto también la hace **testeable**.

`python -m paquete.modulo` ejecuta un módulo como script usando la resolución de imports
del paquete. Es la forma recomendada de correr módulos que están dentro de paquetes, y
también de correr herramientas: `python -m pytest`, `python -m http.server`.

## Paquetes

```
tienda/
├── __init__.py          # se ejecuta al importar "tienda"
├── modelos.py
└── pagos/
    ├── __init__.py
    └── mercadopago.py
```

```python
from tienda.modelos import Producto
from tienda.pagos import mercadopago
```

`__init__.py` puede estar vacío. Suele usarse para exponer la API pública del paquete:

```python
# tienda/__init__.py
from tienda.modelos import Producto, Pedido

__all__ = ["Producto", "Pedido"]
```

`__all__` define qué se exporta con `import *` y documenta la API pública. Por convención,
los nombres que empiezan con `_` son **privados**: nada lo impide, pero indican "no dependas
de esto".

### Imports absolutos vs. relativos

```python
# dentro de tienda/pagos/mercadopago.py
from tienda.modelos import Pedido      # absoluto: recomendado
from ..modelos import Pedido           # relativo: válido solo dentro de un paquete
```

Los relativos no funcionan si ejecutás el archivo directamente (`python mercadopago.py`), y
esa es una fuente clásica de `ImportError: attempted relative import with no known parent
package`. La solución es ejecutarlo como `python -m tienda.pagos.mercadopago`.

## Imports circulares

Si `a.py` importa `b` y `b.py` importa `a`, uno de los dos va a encontrar al otro **a medio
ejecutar**, con nombres que todavía no existen. Soluciones, en orden de preferencia:

1. **Reestructurar**: mover lo compartido a un tercer módulo.
2. Importar el módulo entero (`import a`) en lugar de nombres (`from a import X`) y usar
   `a.X` dentro de las funciones.
3. Importar dentro de la función que lo necesita (último recurso).
4. Si el import es solo para anotaciones de tipo: `if TYPE_CHECKING:`.

## Imports dinámicos

A veces el nombre del módulo recién se conoce al ejecutar (plugins, configuración):

```python
import importlib

modulo = importlib.import_module("json")
funcion = getattr(modulo, "dumps")
```

Así funcionan los strings como `"app.main:app"` que le pasás a uvicorn.

Para consultar metadatos de los paquetes instalados:

```python
from importlib.metadata import version, PackageNotFoundError
version("pytest")        # '8.4.1'
```

## Módulos, entornos y `uv`

Los paquetes de terceros se instalan en `site-packages` **del entorno virtual** activo. Con
`uv`, cada proyecto tiene su `.venv`; `uv add paquete` lo instala y lo registra en
`pyproject.toml`, y `uv run comando` ejecuta con ese entorno. Lo vemos en detalle en el
módulo de herramientas.

## Resumen

- Importar ejecuta el módulo una vez y lo cachea en `sys.modules`.
- No pongas efectos secundarios en el nivel superior; usá `if __name__ == "__main__":` y una
  función `main(argv) -> int`.
- Sin `import *`. Absolutos antes que relativos. `__all__` y `_privado` para la API.
- Imports circulares: reestructurá.
- `importlib.import_module` + `getattr` para imports dinámicos.

## Ejercicio

Cuatro funciones: import dinámico por ruta, listar la API pública de un módulo, consultar
versiones instaladas y un `main` testeable con su guarda.

**Para profundizar:** [The import system](https://docs.python.org/3/reference/import.html),
[Modules (tutorial)](https://docs.python.org/3/tutorial/modules.html).
