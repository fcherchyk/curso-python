# Models and the Django ORM

The ORM is the heart of Django: you define **models** (classes) and Django generates the tables,
migrations, admin and forms from them. Queries are written with a chainable, lazy API, the
**QuerySets**, which covers everything from a simple `filter` to aggregations and expressions
computed in the database.

## Models

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
```

- Each class is a table and each `models.XField` attribute is a column. The autoincrementing
  `id` is added for you.
- `ForeignKey` requires `on_delete`: `CASCADE` (deletes the children), `PROTECT` (prevents
  deletion), `SET_NULL`…
- `related_name` defines the reverse accessor: `category.products.all()`.
- For money, `DecimalField`, never `FloatField`.
- `__str__` defines how the object looks in the admin and in the console.

## Migrations

```bash
uv run python manage.py makemigrations     # generates a file with the model changes
uv run python manage.py migrate            # applies them to the database
```

Migrations are versioned code (`catalog/migrations/0001_initial.py`) and go into git.
Django detects changes on its own: adding a field, renaming one or creating an index.

## QuerySets: chainable, lazy queries

```python
Product.objects.all()
Product.objects.filter(active=True, price__lte=5000)        # AND
Product.objects.exclude(stock=0)
Product.objects.filter(category__name="Pantry")              # follows the FK with __
Product.objects.order_by("-price", "name")                   # - = descending
Product.objects.get(id=3)              # ONE: raises DoesNotExist or MultipleObjectsReturned
Product.objects.filter(...).first()    # the first one or None
Product.objects.count(), .exists()
Product.objects.values("name", "price")          # dicts instead of objects
Product.objects.values_list("name", flat=True)
```

**Lookups** go after a double underscore: `exact`, `iexact`, `contains`, `icontains`,
`in`, `gt`, `gte`, `lt`, `lte`, `startswith`, `isnull`, `range`, `year`…

A QuerySet is **lazy**: it doesn't hit the database until you iterate it, convert it to a list,
slice it with a step or call `len()`. That's why you can chain `filter` calls at no cost.

### OR and NOT: `Q`

```python
from django.db.models import Q

Product.objects.filter(Q(name__icontains="mat") | Q(category__name__icontains="mat"))
Product.objects.filter(~Q(stock=0))
```

## Aggregations and annotations

```python
from django.db.models import Count, Sum, Avg

Product.objects.aggregate(total=Sum("stock"), average=Avg("price"))
# {'total': 120, 'average': Decimal('4500.00')}

Category.objects.annotate(count=Count("products"))            # one computed field per row
Product.objects.values("category__name").annotate(stock=Sum("stock"))   # GROUP BY
```

## Updating in the database: `F` and `update`

```python
from django.db.models import F

Product.objects.filter(category__name="Pantry").update(price=F("price") * 1.10)
```

`F("price")` refers to the value **in the database**: the calculation happens in SQL, in a single
query and with no race conditions. The alternative of fetching each object, modifying it and
calling `save()` is slower and can overwrite concurrent changes.

## Creating, modifying and deleting

```python
cat = Category.objects.create(name="Pantry")
p = Product(name="Mate", price="3500", category=cat)
p.save()                          # INSERT (or UPDATE if it already has an id)
p.stock = 10
p.save(update_fields=["stock"])   # only that field
p.delete()
obj, created = Category.objects.get_or_create(name="Drinks")
```

## The N+1 problem and `select_related` / `prefetch_related`

```python
for p in Product.objects.all():
    print(p.category.name)             # one query per product!
```

```python
Product.objects.select_related("category")            # JOIN: for FK and one-to-one
Category.objects.prefetch_related("products")         # 2 queries: for "many" relationships
```

It's the same problem you saw with SQLAlchemy, and it's the most common performance bug in Django.
`django-debug-toolbar` and, in tests, `assertNumQueries` help you catch it.

## In other frameworks

| Django                                        | SQLAlchemy 2.0                                     |
|-----------------------------------------------|----------------------------------------------------|
| `Product.objects.filter(price__lte=5)`        | `select(Product).where(Product.price <= 5)`        |
| `Q(a) \| Q(b)`                                 | `or_(a, b)`                                        |
| `F("price") * 1.1`                            | `Product.price * 1.1`                              |
| `select_related` / `prefetch_related`         | `joinedload` / `selectinload`                      |
| built-in migrations                           | Alembic                                            |
| active record (`p.save()`)                    | unit of work (`session.add` + `commit`)            |

## Summary

- Models = tables; `ForeignKey` with `on_delete` and `related_name`; `DecimalField` for money.
- `makemigrations` and `migrate`; migrations go into git.
- Lazy QuerySets: `filter`, `exclude`, `order_by`, lookups with `__` and `Q` for OR and NOT.
- `aggregate` and `annotate` to compute in the database; `F` + `update` for bulk changes.
- `select_related`/`prefetch_related` against N+1.

## Exercise

The models are already there. Write query functions: combined filters, a search with `Q`,
an aggregation by category, a price increase with `F` and a listing without N+1 (the tests count
the queries).

**Further reading:** [Models](https://docs.djangoproject.com/en/stable/topics/db/models/),
[Making queries](https://docs.djangoproject.com/en/stable/topics/db/queries/),
[Aggregation](https://docs.djangoproject.com/en/stable/topics/db/aggregation/).
