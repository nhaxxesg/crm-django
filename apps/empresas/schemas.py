from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class EmpresaCreateSchema(BaseModel):
    nombre: str = Field(min_length=2, max_length=200)
    industria: Optional[str] = Field(
        default=None,
        pattern="^(tecnologia|servicios|manufactura|comercio|salud|educacion|otros)$",
    )
    num_empleados: Optional[int] = Field(default=None, gt=0)
    sitio_web: Optional[HttpUrl] = None
    telefono: Optional[str] = Field(default=None, max_length=20)
    direccion: Optional[str] = Field(default=None, max_length=300)
    notas: Optional[str] = Field(default=None, max_length=1000)


class EmpresaUpdateSchema(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=200)
    industria: Optional[str] = Field(
        default=None,
        pattern="^(tecnologia|servicios|manufactura|comercio|salud|educacion|otros)$",
    )
    num_empleados: Optional[int] = Field(default=None, gt=0)
    sitio_web: Optional[HttpUrl] = None
    telefono: Optional[str] = Field(default=None, max_length=20)
    direccion: Optional[str] = Field(default=None, max_length=300)
    notas: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        extra = "forbid"


