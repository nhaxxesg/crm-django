from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, condecimal, validator


ETAPAS_PATTERN = "^(prospeccion|calificacion|propuesta|negociacion|cerrado_ganado|cerrado_perdido)$"
MONEDA_PATTERN = "^(PEN|USD|EUR)$"


class OportunidadCreateSchema(BaseModel):
    nombre: str = Field(min_length=5, max_length=200)
    cliente_id: int = Field(gt=0)
    empresa_id: int = Field(gt=0)
    valor: condecimal(gt=0, max_digits=12, decimal_places=2)
    moneda: str = Field(pattern=MONEDA_PATTERN)
    probabilidad: int = Field(ge=0, le=100)
    fecha_cierre_estimada: date
    etapa: str = Field(pattern=ETAPAS_PATTERN)
    notas: Optional[str] = Field(default=None, max_length=1000)

    @validator("fecha_cierre_estimada")
    def validar_fecha_futura(cls, value: date):
        if value < date.today():
            raise ValueError("La fecha de cierre debe ser futura")
        return value


class OportunidadUpdateSchema(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=5, max_length=200)
    cliente_id: Optional[int] = Field(default=None, gt=0)
    empresa_id: Optional[int] = Field(default=None, gt=0)
    valor: Optional[condecimal(gt=0, max_digits=12, decimal_places=2)] = None
    moneda: Optional[str] = Field(default=None, pattern=MONEDA_PATTERN)
    probabilidad: Optional[int] = Field(default=None, ge=0, le=100)
    fecha_cierre_estimada: Optional[date] = None
    etapa: Optional[str] = Field(default=None, pattern=ETAPAS_PATTERN)
    estado: Optional[str] = Field(default=None, pattern="^(abierta|cerrada)$")
    resultado: Optional[str] = Field(default=None, pattern="^(ganada|perdida)$")
    notas: Optional[str] = Field(default=None, max_length=1000)

    @validator("fecha_cierre_estimada")
    def validar_fecha_futura(cls, value: Optional[date]):
        if value and value < date.today():
            raise ValueError("La fecha de cierre debe ser futura")
        return value

    class Config:
        extra = "forbid"


class ActualizarEtapaSchema(BaseModel):
    etapa: str = Field(pattern=ETAPAS_PATTERN)
    notas: Optional[str] = Field(default=None, max_length=1000)


