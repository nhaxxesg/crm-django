from __future__ import annotations

import django_filters

from .models import Actividad


class ActividadFilter(django_filters.FilterSet):
    fecha_desde = django_filters.DateTimeFilter(field_name="fecha_hora", lookup_expr="gte")
    fecha_hasta = django_filters.DateTimeFilter(field_name="fecha_hora", lookup_expr="lte")
    cliente_id = django_filters.NumberFilter(field_name="cliente_id")
    oportunidad_id = django_filters.NumberFilter(field_name="oportunidad_id")

    class Meta:
        model = Actividad
        fields = ["tipo", "estado"]


