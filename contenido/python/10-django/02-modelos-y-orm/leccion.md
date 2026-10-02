# Modelos y el ORM de Django

El ORM es el corazón de Django: definís **modelos** (clases) y Django genera las tablas, las
migraciones, el admin y los formularios a partir de ellos. Las consultas se escriben con una API
encadenable y perezosa, los **QuerySets**, que cubre desde un `filter` simple hasta agregaciones y
expresiones que se calculan en la base de datos.

## Modelos

```python
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
```

- Cada clase es una tabla y cada atributo `models.XField`, una columna. El `id` autoincremental
  se agrega solo.
- `ForeignKey` necesita `on_delete`: `CASCADE` (borra los hijos), `PROTECT` (impide borrar),
  `SET_NULL`…
- `related_name` define el acceso inverso: `categoria.productos.all()`.
- Para dinero, `DecimalField`, nunca `FloatField`.
- `__str__` define cómo se ve el objeto en el admin y en la consola.

## Migraciones

```bash
uv run python manage.py makemigrations     # genera un archivo con los cambios del modelo
uv run python manage.py migrate            # los aplica a la base
```

Las migraciones son código versionado (`catalogo/migrations/0001_initial.py`) y van a git.
Django detecta los cambios solo: agregar un campo, renombrar o crear un índice.

## QuerySets: consultas encadenables y perezosas

```python
Producto.objects.all()
Producto.objects.filter(activo=True, precio__lte=5000)      # AND
Producto.objects.exclude(stock=0)
Producto.objects.filter(categoria__nombre="Almacén")         # cruza la FK con __
Producto.objects.order_by("-precio", "nombre")               # - = descendente
Producto.objects.get(id=3)              # UNO: levanta DoesNotExist o MultipleObjectsReturned
Producto.objects.filter(...).first()    # el primero o None
Producto.objects.count(), .exists()
Producto.objects.values("nombre", "precio")      # dicts en lugar de objetos
Producto.objects.values_list("nombre", flat=True)
```

Los **lookups** van después de un doble guion bajo: `exact`, `iexact`, `contains`, `icontains`,
`in`, `gt`, `gte`, `lt`, `lte`, `startswith`, `isnull`, `range`, `year`…

Un QuerySet es **perezoso**: no consulta la base hasta que lo recorrés, lo convertís en lista,
lo rebanás con paso o llamás a `len()`. Por eso se pueden encadenar `filter` sin costo.

### OR y NOT: `Q`

```python
from django.db.models import Q

Producto.objects.filter(Q(nombre__icontains="yer") | Q(categoria__nombre__icontains="yer"))
Producto.objects.filter(~Q(stock=0))
```

## Agregaciones y anotaciones

```python
from django.db.models import Count, Sum, Avg

Producto.objects.aggregate(total=Sum("stock"), promedio=Avg("precio"))
# {'total': 120, 'promedio': Decimal('4500.00')}

Categoria.objects.annotate(cantidad=Count("productos"))        # un campo calculado por fila
Producto.objects.values("categoria__nombre").annotate(stock=Sum("stock"))   # GROUP BY
```

## Actualizar en la base: `F` y `update`

```python
from django.db.models import F

Producto.objects.filter(categoria__nombre="Almacén").update(precio=F("precio") * 1.10)
```

`F("precio")` hace referencia al valor **en la base**: el cálculo se hace en SQL, en una sola
consulta y sin condiciones de carrera. La alternativa de traer cada objeto, modificarlo y hacer
`save()` es más lenta y puede pisar cambios concurrentes.

## Crear, modificar y borrar

```python
cat = Categoria.objects.create(nombre="Almacén")
p = Producto(nombre="Yerba", precio="3500", categoria=cat)
p.save()                          # INSERT (o UPDATE si ya tiene id)
p.stock = 10
p.save(update_fields=["stock"])   # solo ese campo
p.delete()
obj, creado = Categoria.objects.get_or_create(nombre="Bebidas")
```

## El problema N+1 y `select_related` / `prefetch_related`

```python
for p in Producto.objects.all():
    print(p.categoria.nombre)          # ¡una consulta por producto!
```

```python
Producto.objects.select_related("categoria")          # JOIN: para FK y one-to-one
Categoria.objects.prefetch_related("productos")       # 2 consultas: para relaciones "muchos"
```

Es el mismo problema que viste con SQLAlchemy y es el error de rendimiento más común en Django.
`django-debug-toolbar` y, en los tests, `assertNumQueries` ayudan a detectarlo.

## En los otros frameworks

| Django                                        | SQLAlchemy 2.0                                     |
|-----------------------------------------------|----------------------------------------------------|
| `Producto.objects.filter(precio__lte=5)`       | `select(Producto).where(Producto.precio <= 5)`     |
| `Q(a) \| Q(b)`                                 | `or_(a, b)`                                        |
| `F("precio") * 1.1`                           | `Producto.precio * 1.1`                            |
| `select_related` / `prefetch_related`         | `joinedload` / `selectinload`                      |
| migraciones incorporadas                      | Alembic                                            |
| active record (`p.save()`)                     | unit of work (`session.add` + `commit`)            |

## Resumen

- Modelos = tablas; `ForeignKey` con `on_delete` y `related_name`; `DecimalField` para dinero.
- `makemigrations` y `migrate`; las migraciones van a git.
- QuerySets perezosos: `filter`, `exclude`, `order_by`, lookups con `__` y `Q` para OR y NOT.
- `aggregate` y `annotate` para calcular en la base; `F` + `update` para modificar en masa.
- `select_related`/`prefetch_related` contra el N+1.

## Ejercicio

Los modelos ya están. Escribí funciones de consulta: filtros combinados, búsqueda con `Q`,
agregación por categoría, un aumento de precios con `F` y un listado sin N+1 (los tests cuentan
las consultas).

**Para profundizar:** [Models](https://docs.djangoproject.com/en/stable/topics/db/models/),
[Making queries](https://docs.djangoproject.com/en/stable/topics/db/queries/),
[Aggregation](https://docs.djangoproject.com/en/stable/topics/db/aggregation/).
