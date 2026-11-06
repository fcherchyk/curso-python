from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator


class Address(BaseModel):
    street: str = Field(min_length=3)
    city: str
    postcode: str = Field(pattern=r"^\d{4}$")


class NewUser(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str
    age: int = Field(ge=0, le=130)
    password: str = Field(min_length=8)
    address: Address | None = None

    # mode="before": the strip runs before the length check.
    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, v: object) -> object:
        return v.strip() if isinstance(v, str) else v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    @model_validator(mode="after")
    def password_differs_from_name(self) -> "NewUser":
        if self.password.lower() == self.name.lower():
            raise ValueError("the password can't be the same as the name")
        return self


class PublicUser(BaseModel):
    id: int
    name: str
    email: str
    age: int


app = FastAPI()
USERS: dict[int, dict[str, object]] = {}


@app.post("/users", response_model=PublicUser, status_code=201)
def create_user(data: NewUser) -> dict[str, object]:
    new_id = len(USERS) + 1
    USERS[new_id] = {"id": new_id, **data.model_dump()}
    return USERS[new_id]  # includes password: response_model filters it out


@app.get("/users/{id}", response_model=PublicUser)
def get_user(id: int) -> dict[str, object]:
    if id not in USERS:
        raise HTTPException(404, "user not found")
    return USERS[id]
