from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


TIPO_PATTERN = "^(llamada|reunion|email|tarea)$"
ESTADO_PATTERN = "^(pendiente|completada|cancelada)$"


class ActividadCreateSchema(BaseModel):
    tipo: str = Field(pattern=TIPO_PATTERN)
    asunto: str = Field(min_length=5, max_length=200)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    fecha_hora: datetime
    estado: str = Field(default="pendiente", pattern=ESTADO_PATTERN)
    cliente_id: Optional[int] = Field(default=None, gt=0)
    oportunidad_id: Optional[int] = Field(default=None, gt=0)
    resultado: Optional[str] = Field(default=None, max_length=500)


class ActividadUpdateSchema(BaseModel):
    tipo: Optional[str] = Field(default=None, pattern=TIPO_PATTERN)
    asunto: Optional[str] = Field(default=None, min_length=5, max_length=200)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    fecha_hora: Optional[datetime] = None
    estado: Optional[str] = Field(default=None, pattern=ESTADO_PATTERN)
    cliente_id: Optional[int] = Field(default=None, gt=0)
    oportunidad_id: Optional[int] = Field(default=None, gt=0)
    resultado: Optional[str] = Field(default=None, max_length=500)

    class Config:
        extra = "forbid"


class ActividadCompletarSchema(BaseModel):
    resultado: str = Field(min_length=5, max_length=500)


