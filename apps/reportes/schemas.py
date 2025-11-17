from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, validator


class VentasQuerySchema(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    agrupar_por: str = Field(default="mes", pattern="^(dia|semana|mes)$")
    moneda: Optional[str] = Field(default=None, pattern="^(PEN|USD|EUR)$")

    @validator("fecha_fin")
    def validar_rango(cls, value: date, values):
        inicio = values.get("fecha_inicio")
        if inicio and value < inicio:
            raise ValueError("fecha_fin debe ser mayor o igual a fecha_inicio")
        return value


