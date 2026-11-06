# Authentication and permissions

Implementing login securely (password hashing, sessions, protection against session fixation,
permissions) is hard and easy to get wrong. Django ships it solved in
`django.contrib.auth`: a user model, hashing with modern algorithms, session-based login and
logout, decorators and mixins to protect views, and a permissions and groups system integrated
with the admin.

## The `User` model

```python
from django.contrib.auth import get_user_model

User = get_user_model()            # never import User directly (it may be a custom one)

u = User.objects.create_user("alice", email="alice@x.com", password="secure-password-123")
u.password                         # 'pbkdf2_sha256$...' ← a HASH, never the plain text
u.check_password("secure-password-123")   # True
u.set_password("other")            # hashes; then you need u.save()
User.objects.create_superuser("admin", password="...")
```

- **Never** store or compare passwords in plain text. `create_user` and `set_password`
  hash with PBKDF2 by default (or Argon2/bcrypt if you configure them), with a *salt* and iterations.
- `is_active`, `is_staff` (can access the admin) and `is_superuser` (all permissions).
- **Golden rule**: in a new project, define your own user from day one
  (`class Account(AbstractUser)` + `AUTH_USER_MODEL = "accounts.Account"`). Changing it later is
  very painful.

## Login and logout

```python
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    user = authenticate(request, username=request.POST["username"],
                        password=request.POST["password"])
    if user is None:
        return JsonResponse({"error": "invalid credentials"}, status=400)
    login(request, user)             # stores the id in the session (and rotates the session)
    return redirect("notes")

def logout_view(request):
    logout(request)                  # clears the session
    ...
```

- `authenticate` checks the credentials against the configured *backends* and returns the user
  or `None`. It does **not** say whether the username or the password was wrong, on purpose.
- `login` attaches the user to the session (it needs `SessionMiddleware` and
  `AuthenticationMiddleware`). After that, in **any** view, `request.user` is the user and
  `request.user.is_authenticated` is `True`.
- Django also ships ready-made views: `LoginView`, `LogoutView`, `PasswordResetView`…
  (`path("accounts/", include("django.contrib.auth.urls"))`).

## Protecting views

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@login_required                                    # not logged in → redirect to LOGIN_URL?next=...
def my_notes(request): ...

@permission_required("notes.delete_note", raise_exception=True)    # no permission → 403
def delete(request, id): ...

class NoteList(LoginRequiredMixin, ListView): ...                  # in CBVs, as a mixin
```

### Object-level authorization

`login_required` answers "who are you?". But the more common question is "is **this** note
yours?", and you answer that in the view:

```python
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

note = get_object_or_404(Note, id=id)
if note.author != request.user and not request.user.is_staff:
    raise PermissionDenied                      # → 403
```

Another very common approach is to **filter the queryset by user**:
`Note.objects.filter(author=request.user)`. That way another user simply gets a 404 and never
learns the note exists.

## Permissions and groups

For each model, Django creates the permissions `add_`, `change_`, `delete_` and `view_<model>`. They
are assigned to users or, better, to **groups** (for example "Editors") from the admin.
`user.has_perm("app.delete_note")` checks them, and custom permissions are declared in
`Meta.permissions`.

## In other frameworks

| Need                          | Django                              | Flask                     | FastAPI                                 |
|-------------------------------|-------------------------------------|---------------------------|-----------------------------------------|
| Users and hashing             | `contrib.auth` included             | Flask-Login + werkzeug.security | by hand or libraries (passlib, pwdlib) |
| Session                       | `login()` + middleware              | Flask-Login               | JWT tokens or OAuth2 (`OAuth2PasswordBearer`) |
| Protecting views              | `@login_required`, mixins           | Flask-Login's `@login_required` | `Depends(current_user)`           |
| Permissions                   | permissions + groups + admin        | by hand                   | by hand (dependencies)                  |
| APIs                          | DRF: `IsAuthenticated`, tokens      | by hand                   | dependencies                            |

## Testing with users

```python
def test_my_notes(client):                       # pytest-django, or django.test.Client
    user = User.objects.create_user("alice", password="x")
    client.force_login(user)                     # without going through the login form
    r = client.get("/notes/")
```

`force_login` saves you from repeating the login in every test. In tests, use a fast hasher
(`PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]`): PBKDF2 is slow on
purpose.

## Summary

- `get_user_model()`, `create_user` and `check_password`: passwords are always hashed.
- `authenticate` + `login`/`logout`; afterwards, `request.user` in every view.
- `@login_required` (redirects to the login) and `LoginRequiredMixin`; `permission_required` for
  permissions.
- Object-level authorization: compare the owner or filter the queryset by `request.user`;
  `PermissionDenied` → 403.
- Automatic per-model permissions and groups from the admin; `force_login` in tests.

## Exercise

User registration, session-based login and logout, private per-user notes protected with
`login_required`, and deletion only for the owner or staff.

**Further reading:** [User authentication in Django](https://docs.djangoproject.com/en/stable/topics/auth/default/),
[Password management](https://docs.djangoproject.com/en/stable/topics/auth/passwords/),
[Customizing authentication](https://docs.djangoproject.com/en/stable/topics/auth/customizing/).
