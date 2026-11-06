# Pydantic: validating data with types

Pydantic is Python's most widely used validation library, and it's the heart of FastAPI. You
declare a **model** with type hints, and Pydantic **validates, converts and serializes** the
data coming in from outside (an API's JSON, config files, environment variables). If something
doesn't fit, it gives you detailed per-field errors. That's the difference from the
dataclasses in module 05: those **don't validate** anything.

## A model

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    tags: list[str] = []          # with a default: optional (Pydantic copies the default, no trap here)
    description: str | None = None

p = Product(name="mate", price="3500")          # "3500" is converted to 3500.0
p.price                                         # 3500.0
p.model_dump()                                  # dict
p.model_dump_json()                             # JSON (str)
Product.model_validate({"name": "coffee", "price": 10})   # from a dict
Product.model_validate_json('{"name": "tea", "price": 5}')
```

If the data is no good, it raises `ValidationError` with **all** the problems together:

```python
Product(name="x", price="expensive")
# ValidationError: 1 validation error for Product
# price
#   Input should be a valid number, unable to parse string as a number
```

By default Pydantic runs in **lax mode**: it converts `"3500"` into `3500`. With
`model_config = ConfigDict(strict=True)` (or `Field(strict=True)` on a field) it requires the
exact type.

## Constraints with `Field`

```python
from typing import Annotated
from pydantic import BaseModel, Field

class NewUser(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0, le=130)               # ≥ 0 and ≤ 130
    password: str = Field(min_length=8)
    postcode: str = Field(pattern=r"^\d{4}$")     # regex
    price: Annotated[float, Field(gt=0)]          # equivalent form with Annotated
```

Typical constraints: `gt`/`ge`/`lt`/`le` for numbers, `min_length`/`max_length` for strings
and lists, `pattern` for regex, and `default`/`default_factory`. For emails, `EmailStr` (needs
`pip install "pydantic[email]"`).

## Custom validators

```python
from pydantic import field_validator, model_validator

class NewUser(BaseModel):
    name: str
    email: str
    password: str

    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, v: object) -> object:
        return v.strip() if isinstance(v, str) else v   # it can TRANSFORM the value…

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")   # …or reject it
        return v.lower()

    @model_validator(mode="after")
    def password_differs_from_name(self) -> "NewUser":
        if self.password.lower() == self.name.lower():
            raise ValueError("the password can't be the same as the name")
        return self
```

- `field_validator` validates **one field**; it returns the value (transformed or not) or
  raises `ValueError`.
- `model_validator(mode="after")` validates **cross-field rules**, with the model already built.
- Order matters. With `mode="after"` (the default), your validator runs **after** the type
  and `Field` constraints. With `mode="before"`, it runs **before**, on the raw data (which may
  not be a `str`). That's why the `strip` in the example is `before`: that way `min_length` is
  checked on the already-cleaned name.

## Nested models

```python
class Address(BaseModel):
    street: str
    city: str

class Customer(BaseModel):
    name: str
    address: Address                     # validated recursively
    others: list[Address] = []
```

Errors show the full path: `address.city: Field required`.

## Pydantic in FastAPI

FastAPI uses models in both directions:

```python
class PublicUser(BaseModel):              # what you RETURN (no password)
    id: int
    name: str
    email: str

@app.post("/users", response_model=PublicUser, status_code=201)
def create(data: NewUser):                 # what you RECEIVE (validated)
    user = {"id": 1, **data.model_dump()}
    return user                            # includes password…
                                           # …but response_model FILTERS it out
```

- A model-typed parameter is the **body**. If it doesn't validate, FastAPI responds **422**
  with the list of errors (`loc`, `msg`, `type`) without entering your function.
- `response_model` (or the annotated return type) **filters and validates the output**: even
  if you return a dict with `password`, the response only has the fields of `PublicUser`. It's
  the idiomatic way to avoid leaking sensitive data.
- The usual pattern is **one model per use case**: `XCreate` (input), `XUpdate` (with optional
  fields) and `XPublic` (output).

## Serialization

```python
p.model_dump(exclude={"password"})
p.model_dump(exclude_none=True)           # without the None fields
p.model_dump(mode="json")                 # JSON-compatible types (dates to strings, etc.)
p.model_copy(update={"price": 10})        # copy with changes
```

## In the other frameworks

- **Flask** has no built-in validation: you do it by hand, or with Pydantic, marshmallow or
  WTForms.
- **Django** validates with `Form` (HTML), and Django REST Framework with `Serializer`: the
  same idea with a different syntax.
- Pydantic is also used outside the web: `pydantic-settings` reads typed configuration from
  environment variables.

## Summary

- `BaseModel` + type hints = validation and conversion; `ValidationError` reports every error.
- `Field(...)` for constraints (`ge`, `min_length`, `pattern`…).
- `field_validator` for one field; `model_validator(mode="after")` for cross-field rules.
- Nested models and lists of models are validated recursively.
- In FastAPI: model as a parameter = validated body (422 if it fails); `response_model`
  filters the output.

## Exercise

User models with constraints, normalization, a cross-field rule and an API that never returns
the password.

**Further reading:** [Pydantic: Models](https://docs.pydantic.dev/latest/concepts/models/),
[Validators](https://docs.pydantic.dev/latest/concepts/validators/),
[FastAPI: Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
