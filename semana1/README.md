# Semana 1: Sintaxis moderna e idiomática

Unas 6 horas en total, con 1 hora por día. Cada día se apoya en el anterior.

| Día | Carpeta             | Tema                                                     | Tests |
|-----|---------------------|----------------------------------------------------------|-------|
| 1   | `dia1_idiomatico`   | comprehensions, unpacking, zip/enumerate, sort, firmas, dicts | 13 |
| 2   | `dia2_iteradores`   | protocolo de iteración, generadores, pipelines perezosos, itertools | 11 |
| 3   | `dia3_funciones`    | closures, decoradores (con y sin parámetros), context managers | 13 |
| 4   | `dia4_modelado`     | dataclasses, StrEnum, dunder methods, Protocol, genéricos 3.12 | 15 |
| 5   | `dia5_novedades`    | match/case, walrus, ExceptionGroup/except*, f-strings, tomllib | 28 |
| 6   | `dia6_proyecto`     | proyecto: analizador de logs con CLI + ruff + mypy       | 15 |

## Checklist

- [ ] Setup: `uv sync` y `uv run pytest` corre (en rojo)
- [ ] Día 1: `uv run pytest semana1/dia1_idiomatico` en verde
- [ ] Día 2: `uv run pytest semana1/dia2_iteradores` en verde
- [ ] Día 3: `uv run pytest semana1/dia3_funciones` en verde
- [ ] Día 4: `uv run pytest semana1/dia4_modelado` en verde
- [ ] Día 5: `uv run pytest semana1/dia5_novedades` en verde
- [ ] Día 6: tests en verde y la CLI corre sobre `access.log`
- [ ] Día 6: `ruff check` y `mypy --strict` limpios en el proyecto
- [ ] Bonus: al menos 3 "Retos extra"

## Autoevaluación de fin de semana

Si podés responder esto sin mirar, la semana cumplió su objetivo:

1. ¿Qué diferencia hay entre un iterable y un iterador? ¿Por qué `CuentaRegresiva` se puede
   recorrer dos veces y un generador no?
2. ¿Por qué `def f(x, acc=[])` es un bug? ¿Y por qué `field(default_factory=list)`?
3. ¿Qué hace `functools.wraps` y qué se rompe si no lo usás?
4. ¿Cuándo usarías `@contextmanager` y cuándo una clase con `__enter__`/`__exit__`?
5. En un `case`, ¿qué diferencia hay entre `case ROJO:` y `case Color.ROJO:`?
6. ¿Protocol o clase base abstracta? ¿Qué cambia para quien implementa?
7. ¿Qué te da `frozen=True` además de inmutabilidad?
