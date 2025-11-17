from __future__ import annotations

from collections import OrderedDict
from decimal import Decimal
from typing import Dict, Iterable, Tuple, Type

from django.utils import timezone
from rest_framework import serializers

from .models import Oportunidad


class OportunidadService:
    """Aplicamos Service Layer para mantener reglas de negocio cohesionadas."""

    @staticmethod
    def actualizar_etapa(oportunidad: Oportunidad, etapa: str, notas: str | None = None) -> Oportunidad:
        oportunidad.etapa = etapa
        if etapa in {"cerrado_ganado", "cerrado_perdido"}:
            oportunidad.estado = "cerrada"
            oportunidad.resultado = "ganada" if etapa == "cerrado_ganado" else "perdida"
            oportunidad.fecha_cierre_real = timezone.now()
        else:
            oportunidad.estado = "abierta"
            oportunidad.resultado = None
            oportunidad.fecha_cierre_real = None
        if notas is not None:
            oportunidad.notas = notas
        oportunidad.save()
        return oportunidad

    @staticmethod
    def build_pipeline(
        oportunidades: Iterable[Oportunidad],
        serializer_cls: Type[serializers.ModelSerializer],
    ) -> Tuple[Dict[str, Dict[str, object]], int, float]:
        items = list(oportunidades)
        serialized = serializer_cls(items, many=True).data

        etapas = {}
        total_valor = Decimal("0")
        for obj, payload in zip(items, serialized):
            stage = obj.etapa
            bucket = etapas.setdefault(stage, {"count": 0, "valor_total": Decimal("0"), "oportunidades": []})
            bucket["count"] += 1
            bucket["valor_total"] += Decimal(obj.valor)
            bucket["oportunidades"].append(payload)
            total_valor += Decimal(obj.valor)

        ordered = OrderedDict()
        for stage, _ in Oportunidad.ETAPAS:
            if stage in etapas:
                ordered[stage] = etapas[stage]

        for payload in ordered.values():
            payload["valor_total"] = float(payload["valor_total"])

        return ordered, len(items), float(total_valor)


