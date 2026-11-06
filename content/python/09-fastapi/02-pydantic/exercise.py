"""Pydantic: validating data with types.

1. Address: street (str, min. 3 characters), city (str), postcode (str of exactly 4 digits).
2. NewUser:
   - name: 2 to 50 characters, WITHOUT surrounding whitespace (field_validator that strips;
     the length is validated after the strip)
   - email: must contain "@"; stored in lowercase (field_validator)
   - age: between 0 and 130
   - password: at least 8 characters
   - address: Address | None = None
   - cross-field rule (model_validator): password different from the name (case
     insensitive) → otherwise, ValueError("the password can't be the same as the name")
3. PublicUser: id, name, email, age (no password or address).
4. POST /users: body NewUser → 201 with PublicUser (response_model), incremental id.
   GET  /users/{id}: PublicUser or 404.
"""

from fastapi import FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel, Field, field_validator, model_validator  # noqa: F401


class Address(BaseModel):
    street: str
    city: str
    postcode: str


class NewUser(BaseModel):
    name: str
    email: str
    age: int
    password: str
    address: Address | None = None


class PublicUser(BaseModel):
    id: int
    name: str
    email: str
    age: int


app = FastAPI()
USERS: dict[int, dict[str, object]] = {}
