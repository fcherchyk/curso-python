# Autenticación y permisos

Implementar login de forma segura (hash de contraseñas, sesiones, protección contra fijación de
sesión, permisos) es difícil y fácil de hacer mal. Django lo trae resuelto en
`django.contrib.auth`: modelo de usuario, hashing con algoritmos modernos, login y logout
basados en la sesión, decoradores y mixins para proteger vistas, y un sistema de permisos y
grupos integrado con el admin.

## El modelo `User`

```python
from django.contrib.auth import get_user_model

User = get_user_model()            # nunca importes User directamente (puede ser uno propio)

u = User.objects.create_user("ana", email="ana@x.com", password="clave-segura-123")
u.password                         # 'pbkdf2_sha256$...' ← HASH, nunca el texto plano
u.check_password("clave-segura-123")   # True
u.set_password("otra")             # hashea; después hay que hacer u.save()
User.objects.create_superuser("admin", password="...")
```

- **Nunca** guardes ni compares contraseñas en texto plano. `create_user` y `set_password`
  hashean con PBKDF2 por defecto (o Argon2/bcrypt si los configurás), con *salt* e iteraciones.
- `is_active`, `is_staff` (puede entrar al admin) e `is_superuser` (todos los permisos).
- **Consejo de oro**: en un proyecto nuevo, definí un usuario propio desde el día uno
  (`class Usuario(AbstractUser)` + `AUTH_USER_MODEL = "cuentas.Usuario"`). Cambiarlo después es
  muy doloroso.

## Login y logout

```python
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    usuario = authenticate(request, username=request.POST["username"],
                           password=request.POST["password"])
    if usuario is None:
        return JsonResponse({"error": "credenciales inválidas"}, status=400)
    login(request, usuario)          # guarda el id en la sesión (y rota la sesión)
    return redirect("notas")

def logout_view(request):
    logout(request)                  # borra la sesión
    ...
```

- `authenticate` verifica las credenciales con los *backends* configurados y devuelve el usuario
  o `None`. **No** dice si falló el usuario o la contraseña, a propósito.
- `login` asocia el usuario a la sesión (necesita `SessionMiddleware` y
  `AuthenticationMiddleware`). Después, en **cualquier** vista, `request.user` es el usuario y
  `request.user.is_authenticated` vale `True`.
- Django también trae vistas listas: `LoginView`, `LogoutView`, `PasswordResetView`…
  (`path("cuentas/", include("django.contrib.auth.urls"))`).

## Proteger vistas

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@login_required                                    # sin login → redirect a LOGIN_URL?next=...
def mis_notas(request): ...

@permission_required("notas.delete_nota", raise_exception=True)    # sin permiso → 403
def borrar(request, id): ...

class NotaLista(LoginRequiredMixin, ListView): ...                 # en CBV, como mixin
```

### Autorización a nivel de objeto

`login_required` responde a "¿quién sos?". Pero la pregunta más común es "¿**esta** nota es
tuya?", y eso lo resolvés en la vista:

```python
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

nota = get_object_or_404(Nota, id=id)
if nota.autor != request.user and not request.user.is_staff:
    raise PermissionDenied                      # → 403
```

Otra forma, muy común, es **filtrar el queryset por usuario**:
`Nota.objects.filter(autor=request.user)`. Así otro usuario directamente recibe un 404 y ni se
entera de que la nota existe.

## Permisos y grupos

Por cada modelo, Django crea los permisos `add_`, `change_`, `delete_` y `view_<modelo>`. Se
asignan a usuarios o, mejor, a **grupos** (por ejemplo "Editores") desde el admin.
`user.has_perm("app.delete_nota")` los consulta, y los permisos propios se declaran en
`Meta.permissions`.

## En los otros frameworks

| Necesidad                     | Django                              | Flask                     | FastAPI                                 |
|-------------------------------|-------------------------------------|---------------------------|-----------------------------------------|
| Usuarios y hashing            | `contrib.auth` incluido             | Flask-Login + werkzeug.security | a mano o librerías (passlib, pwdlib) |
| Sesión                        | `login()` + middleware              | Flask-Login               | tokens JWT u OAuth2 (`OAuth2PasswordBearer`) |
| Proteger vistas               | `@login_required`, mixins           | `@login_required` de Flask-Login | `Depends(usuario_actual)`         |
| Permisos                      | permisos + grupos + admin           | a mano                    | a mano (dependencias)                   |
| APIs                          | DRF: `IsAuthenticated`, tokens      | a mano                    | dependencias                             |

## Testear con usuarios

```python
def test_mis_notas(client):                      # pytest-django, o django.test.Client
    usuario = User.objects.create_user("ana", password="x")
    client.force_login(usuario)                  # sin pasar por el formulario de login
    r = client.get("/notas/")
```

`force_login` evita repetir el login en cada test. En los tests conviene un hasher rápido
(`PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]`): PBKDF2 es lento a
propósito.

## Resumen

- `get_user_model()`, `create_user` y `check_password`: las contraseñas siempre hasheadas.
- `authenticate` + `login`/`logout`; después, `request.user` en todas las vistas.
- `@login_required` (redirige al login) y `LoginRequiredMixin`; `permission_required` para
  permisos.
- Autorización por objeto: compará el dueño o filtrá el queryset por `request.user`;
  `PermissionDenied` → 403.
- Permisos automáticos por modelo y grupos desde el admin; `force_login` en los tests.

## Ejercicio

Registro de usuarios, login y logout con sesión, notas privadas por usuario protegidas con
`login_required` y borrado solo para el dueño o el staff.

**Para profundizar:** [User authentication in Django](https://docs.djangoproject.com/en/stable/topics/auth/default/),
[Password management](https://docs.djangoproject.com/en/stable/topics/auth/passwords/),
[Customizing authentication](https://docs.djangoproject.com/en/stable/topics/auth/customizing/).
