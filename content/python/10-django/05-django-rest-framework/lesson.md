# Django REST Framework

Django was born for apps that return HTML. For **REST APIs**, the de facto standard is **Django
REST Framework (DRF)**: it adds serializers (validation and conversion, like Pydantic), views and
viewsets for APIs, routers that generate the URLs, authentication, permissions, pagination and a
browsable API you can use from the browser. If you already have a Django project, it's the natural
way to expose an API.

```bash
uv add djangorestframework
# settings.py → INSTALLED_APPS += ["rest_framework"]
```

## Serializers: models ↔ JSON, with validation

```python
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "done", "created"]
        read_only_fields = ["id", "created"]

    def validate_title(self, value: str) -> str:           # validate_<field>
        if value.strip().lower() == "todo":
            raise serializers.ValidationError("Use a descriptive title")
        return value.strip()

    def validate(self, data):                                # rules across fields
        ...
        return data
```

It works in both directions:

```python
# object → dict (to respond)
TaskSerializer(task).data                    # {"id": 1, "title": "...", ...}
TaskSerializer(qs, many=True).data           # list

# dict → validated object (to create or update)
s = TaskSerializer(data=request.data)
s.is_valid(raise_exception=True)             # 400 with the errors if it fails
task = s.save()                              # create() or update()
```

It's the equivalent of Pydantic schemas plus Django's `ModelForm`. The
`read_only_fields` are returned, but ignored if they come in the request (like the `id`).

## Views: from `APIView` to `ViewSet`

### `APIView`: full control

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class Stats(APIView):
    def get(self, request):
        return Response({"total": Task.objects.count()})
```

`Response` negotiates the format (JSON or the browsable API) and `request.data` holds the already
parsed body, whether JSON or form.

### `ModelViewSet`: full CRUD in a few lines

```python
from rest_framework import viewsets
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.order_by("id")
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        done = self.request.query_params.get("done")
        if done is not None:
            qs = qs.filter(done=done == "true")
        return qs

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):         # POST /tasks/{pk}/complete/
        task = self.get_object()                  # 404 if it doesn't exist
        task.done = True
        task.save()
        return Response(self.get_serializer(task).data)
```

A `ModelViewSet` gives you `list`, `create`, `retrieve`, `update`, `partial_update` and `destroy`,
with validation, correct status codes (201, 204, 400, 404) and everything else. `@action` adds
extra endpoints to the resource.

### Routers: the URLs generate themselves

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tasks", TaskViewSet)
urlpatterns = [path("api/", include(router.urls))]
```

| Method and URL                      | Viewset action     |
|-------------------------------------|--------------------|
| `GET /api/tasks/`                   | `list`             |
| `POST /api/tasks/`                  | `create`           |
| `GET /api/tasks/{pk}/`              | `retrieve`         |
| `PUT` / `PATCH /api/tasks/{pk}/`    | `update` / `partial_update` |
| `DELETE /api/tasks/{pk}/`           | `destroy`          |
| `POST /api/tasks/{pk}/complete/`    | `@action`          |

## Authentication, permissions, pagination and filters

They're configured globally in `settings.REST_FRAMEWORK` or per view:

```python
from rest_framework.permissions import IsAuthenticated

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # pagination_class = PageNumberPagination
```

We cover this in the next chapter along with Django's users.

## Testing with `APIClient`

```python
from rest_framework.test import APIClient

c = APIClient()
r = c.post("/api/tasks/", {"title": "shopping"}, format="json")
assert r.status_code == 201
assert r.json()["done"] is False
c.force_authenticate(user=user)           # authenticate without going through login
```

## Comparison

| DRF                              | FastAPI                                    |
|----------------------------------|--------------------------------------------|
| `ModelSerializer`                | Pydantic models (Create, Public…)          |
| `validate_<field>` / `validate`  | `field_validator` / `model_validator`      |
| `ModelViewSet` + router          | endpoints written one by one, with `APIRouter` |
| `permission_classes`             | dependencies (`Depends(admin_only)`)       |
| browsable API                    | `/docs` (OpenAPI)                          |
| synchronous, Django ORM          | async, your choice (SQLAlchemy, etc.)      |

## Summary

- Serializers: object ↔ JSON, with validation (`validate_<field>`, `validate`) and
  `read_only_fields`.
- `APIView` for full control; `ModelViewSet` for standard CRUD; `@action` for the extras.
- `DefaultRouter` generates the resource's URLs.
- `request.data`, `query_params` and `Response`.
- `APIClient` for testing (`format="json"`, `force_authenticate`).

## Exercise

A tasks API with DRF: a serializer with validation, a viewset with a filter and an extra
action, a router and a stats view.

**Further reading:** [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/),
[Serializers](https://www.django-rest-framework.org/api-guide/serializers/),
[ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/).
