from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, validator


class RegisterSchema(BaseModel):
    nombre_completo: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6)
    password_confirm: str = Field(min_length=6)
    tipo: str = Field(pattern="^(admin|regular)$")

    @validator("password_confirm")
    def passwords_match(cls, value: str, values):
        if "password" in values and value != values["password"]:
            raise ValueError("Las contraseñas no coinciden")
        return value


class LoginSchema(BaseModel):
    username: str
    password: str



