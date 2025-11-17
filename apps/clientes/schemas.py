from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

from common.validators import validate_phone


class ClienteCreateSchema(BaseModel):
    nombre_completo: str = Field(min_length=3, max_length=150)
    empresa_id: int = Field(gt=0)
    cargo: Optional[str] = Field(default=None, max_length=100)
    telefono: str = Field(min_length=7, max_length=20)
    email: EmailStr
    direccion: Optional[str] = Field(default=None, max_length=300)
    notas: Optional[str] = Field(default=None, max_length=1000)

    @validator("telefono")
    def validar_telefono(cls, value: str):
        if not validate_phone(value):
            raise ValueError("El teléfono debe comenzar con + o 0")
        return value


class ClienteUpdateSchema(BaseModel):
    nombre_completo: Optional[str] = Field(default=None, min_length=3, max_length=150)
    empresa_id: Optional[int] = Field(default=None, gt=0)
    cargo: Optional[str] = Field(default=None, max_length=100)
    telefono: Optional[str] = Field(default=None, min_length=7, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = Field(default=None, max_length=300)
    notas: Optional[str] = Field(default=None, max_length=1000)

    @validator("telefono")
    def validar_telefono(cls, value: Optional[str]):
        if value and not validate_phone(value):
            raise ValueError("El teléfono debe comenzar con + o 0")
        return value

    class Config:
        extra = "forbid"


