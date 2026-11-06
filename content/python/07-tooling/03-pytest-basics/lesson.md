# pytest: tests, asserts y parametrize

Venís usando pytest en cada ejercicio del curso. En este capítulo cambiamos de rol: **vos
escribís los tests**. pytest es el framework de testing estándar de facto: tests como
funciones comunes, `assert` plano con mensajes detallados y un sistema de fixtures y plugins
muy potente.

## Lo mínimo

```python
# tests/test_calendario.py
from calendario import es_bisiesto

def test_2024_es_bisiesto():
    assert es_bisiesto(2024)

def test_2023_no_es_bisiesto():
    assert not es_bisiesto(2023)
```

```bash
uv run pytest
```

Convenciones de descubrimiento:

- Archivos `test_*.py` o `*_test.py`.
- Funciones `test_*` (o métodos `test_*` dentro de clases `Test*` sin `__init__`).
- `testpaths` en `[tool.pytest.ini_options]` define dónde buscar.

## `assert` con introspección

No hay `assertEqual`, `assertTrue` ni similares: se usa `assert` común, y pytest **reescribe**
la expresión para mostrarte qué falló:

```
>       assert dias_del_mes(2023, 2) == 29
E       assert 28 == 29
E        +  where 28 = dias_del_mes(2023, 2)
```

Con listas, dicts y strings muestra la **diferencia** exacta. Podés agregar un mensaje:
`assert x == y, "explicación"`.

Para floats, `pytest.approx`:

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
assert resultado == pytest.approx([1.0, 2.5], rel=1e-3)
```

## Verificar excepciones: `pytest.raises`

```python
import pytest

def test_mes_invalido():
    with pytest.raises(ValueError, match="mes inválido"):
        dias_del_mes(2024, 13)

def test_detalle_de_la_excepcion():
    with pytest.raises(ValueError) as info:
        dias_del_mes(2024, 0)
    assert "0" in str(info.value)
```

`match` es una **regex** que se busca en el mensaje. El test falla si no se levanta la
excepción, o si se levanta otra.

## `parametrize`: un test, muchos casos

```python
@pytest.mark.parametrize(
    ("anio", "esperado"),
    [
        (2024, True),     # divisible por 4
        (2023, False),
        (1900, False),    # divisible por 100 pero no por 400
        (2000, True),     # divisible por 400
    ],
)
def test_es_bisiesto(anio, esperado):
    assert es_bisiesto(anio) is esperado
```

Cada tupla genera un test independiente, con su propio resultado en el reporte
(`test_es_bisiesto[1900-False]`). Es la mejor forma de cubrir **casos borde** sin copiar y
pegar. Con `ids=[...]` o `pytest.param(..., id="siglo")` les das nombres legibles.

## Qué testear

Un buen conjunto de tests cubre:

1. **El caso feliz**: la entrada típica.
2. **Los bordes**: 0, vacío, un elemento, el máximo, el primero y el último.
3. **Las reglas de negocio**, cada una por separado: en `es_bisiesto` hay **tres** reglas
   (cada 4, excepto cada 100, excepto cada 400). Si no testeás 1900 y 2000, dos de ellas
   pueden estar mal y los tests siguen en verde.
4. **Los errores**: entradas inválidas que tienen que levantar excepciones.

Estructura de cada test: **Arrange, Act, Assert** (preparar, ejecutar, verificar). Un test
debería verificar **un comportamiento** y tener un nombre que diga cuál:
`test_febrero_de_bisiesto_tiene_29`.

### ¿Cómo sé si mis tests son buenos? Mutation testing

La **cobertura** (`pytest --cov`) mide qué líneas se ejecutaron, pero no si verificaste algo.
El *mutation testing* es más exigente: introduce bugs a propósito (los **mutantes**, como
cambiar un `<=` por `<` o borrar una condición) y comprueba que **algún test falle**. Si un
mutante "sobrevive", a tus tests les falta un caso. Herramientas: `mutmut` y `cosmic-ray`.

El ejercicio de este capítulo funciona exactamente así.

## Correr pytest como un profesional

```bash
uv run pytest -x                 # frena en el primer fallo
uv run pytest -k bisiesto        # solo tests cuyo nombre contenga "bisiesto"
uv run pytest --lf               # solo los que fallaron la última vez
uv run pytest -v                 # un renglón por test
uv run pytest -q                 # silencioso
uv run pytest tests/test_x.py::test_y   # un test puntual
uv run pytest --pdb              # abre el debugger en el fallo
```

### Marcas útiles

```python
@pytest.mark.skip(reason="depende de la red")
@pytest.mark.skipif(sys.platform == "win32", reason="solo unix")
@pytest.mark.xfail(reason="bug conocido #123")    # se espera que falle
```

## Resumen

- Funciones `test_*` en archivos `test_*.py` con `assert` plano.
- `pytest.raises(Tipo, match=...)` para excepciones; `pytest.approx` para floats.
- `@pytest.mark.parametrize` para cubrir muchos casos, en especial los bordes.
- Testeá cada regla por separado: la cobertura no alcanza, pensá en qué mutantes matarías.
- `-x`, `-k`, `--lf` y `-v` para el día a día.

## Ejercicio

En la pestaña Código **escribís los tests** para `calendario.py` (`es_bisiesto` y
`dias_del_mes`). Requisitos: al menos 4 tests, usar `parametrize` y `pytest.raises`. Tus tests
se corren contra el código correcto (tienen que pasar) y contra **5 mutantes** (cada uno
tiene que hacer fallar al menos uno de tus tests).

```python
# calendario.py (lo que tenés que testear)
def es_bisiesto(anio: int) -> bool:
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)

def dias_del_mes(anio: int, mes: int) -> int:
    if not 1 <= mes <= 12:
        raise ValueError(f"mes inválido: {mes}")
    if mes == 2:
        return 29 if es_bisiesto(anio) else 28
    return 30 if mes in (4, 6, 9, 11) else 31
```

**Para profundizar:** [documentación de pytest](https://docs.pytest.org/en/stable/),
[parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html),
[mutmut](https://mutmut.readthedocs.io/).
