# Django REST Framework

Django nació para apps que devuelven HTML. Para **APIs REST**, el estándar de facto es **Django
REST Framework (DRF)**: agrega serializers (validación y conversión, como Pydantic), vistas y
viewsets para APIs, routers que generan las URLs, autenticación, permisos, paginación y una
API navegable desde el navegador. Si ya tenés un proyecto Django, es la forma natural de
exponer una API.

```bash
uv add djangorestframework
# settings.py → INSTALLED_APPS += ["rest_framework"]
```

## Serializers: modelos ↔ JSON, con validación

```python
from rest_framework import serializers

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ["id", "titulo", "hecha", "creada"]
        read_only_fields = ["id", "creada"]

    def validate_titulo(self, valor: str) -> str:          # validate_<campo>
        if valor.strip().lower() == "todo":
            raise serializers.ValidationError("Poné un título descriptivo")
        return valor.strip()

    def validate(self, datos):                               # reglas entre campos
        ...
        return datos
```

Cumple las dos direcciones:

```python
# objeto → dict (para responder)
TareaSerializer(tarea).data                  # {"id": 1, "titulo": "...", ...}
TareaSerializer(qs, many=True).data          # lista

# dict → objeto validado (para crear o actualizar)
s = TareaSerializer(data=request.data)
s.is_valid(raise_exception=True)             # 400 con los errores si falla
tarea = s.save()                             # create() o update()
```

Es el equivalente de los schemas de Pydantic más el `ModelForm` de Django. Los
`read_only_fields` se devuelven, pero se ignoran si vienen en el request (como el `id`).

## Vistas: de `APIView` a `ViewSet`

### `APIView`: control total

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class Estadisticas(APIView):
    def get(self, request):
        return Response({"total": Tarea.objects.count()})
```

`Response` negocia el formato (JSON o la API navegable) y `request.data` trae el body ya
parseado, sea JSON o formulario.

### `ModelViewSet`: CRUD completo en pocas líneas

```python
from rest_framework import viewsets
from rest_framework.decorators import action

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.order_by("id")
    serializer_class = TareaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        hecha = self.request.query_params.get("hecha")
        if hecha is not None:
            qs = qs.filter(hecha=hecha == "true")
        return qs

    @action(detail=True, methods=["post"])
    def completar(self, request, pk=None):        # POST /tareas/{pk}/completar/
        tarea = self.get_object()                 # 404 si no existe
        tarea.hecha = True
        tarea.save()
        return Response(self.get_serializer(tarea).data)
```

Un `ModelViewSet` da `list`, `create`, `retrieve`, `update`, `partial_update` y `destroy`, con
validación, códigos de estado correctos (201, 204, 400, 404) y todo lo demás. `@action` agrega
endpoints extra al recurso.

### Routers: las URLs se generan solas

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tareas", TareaViewSet)
urlpatterns = [path("api/", include(router.urls))]
```

| Método y URL                        | Acción del viewset |
|-------------------------------------|--------------------|
| `GET /api/tareas/`                  | `list`             |
| `POST /api/tareas/`                 | `create`           |
| `GET /api/tareas/{pk}/`             | `retrieve`         |
| `PUT` / `PATCH /api/tareas/{pk}/`   | `update` / `partial_update` |
| `DELETE /api/tareas/{pk}/`          | `destroy`          |
| `POST /api/tareas/{pk}/completar/`  | `@action`          |

## Autenticación, permisos, paginación y filtros

Se configuran globalmente en `settings.REST_FRAMEWORK` o por vista:

```python
from rest_framework.permissions import IsAuthenticated

class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # pagination_class = PageNumberPagination
```

Lo vemos en el próximo capítulo junto con los usuarios de Django.

## Testear con `APIClient`

```python
from rest_framework.test import APIClient

c = APIClient()
r = c.post("/api/tareas/", {"titulo": "comprar"}, format="json")
assert r.status_code == 201
assert r.json()["hecha"] is False
c.force_authenticate(user=usuario)        # autenticar sin pasar por el login
```

## Comparación

| DRF                              | FastAPI                                    |
|----------------------------------|--------------------------------------------|
| `ModelSerializer`                | modelos Pydantic (Crear, Publica…)         |
| `validate_<campo>` / `validate`  | `field_validator` / `model_validator`      |
| `ModelViewSet` + router          | endpoints escritos uno por uno, con `APIRouter` |
| `permission_classes`             | dependencias (`Depends(solo_admin)`)       |
| API navegable                    | `/docs` (OpenAPI)                          |
| sincrónico, ORM de Django        | async, a elección (SQLAlchemy, etc.)       |

## Resumen

- Serializers: objeto ↔ JSON, con validación (`validate_<campo>`, `validate`) y
  `read_only_fields`.
- `APIView` para control total; `ModelViewSet` para el CRUD estándar; `@action` para los extras.
- `DefaultRouter` genera las URLs del recurso.
- `request.data`, `query_params` y `Response`.
- `APIClient` para testear (`format="json"`, `force_authenticate`).

## Ejercicio

Una API de tareas con DRF: un serializer con validación, un viewset con filtro y una acción
extra, un router y una vista de estadísticas.

**Para profundizar:** [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/),
[Serializers](https://www.django-rest-framework.org/api-guide/serializers/),
[ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/).
