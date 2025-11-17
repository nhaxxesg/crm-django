from __future__ import annotations

import django_filters

from .models import Oportunidad


class OportunidadFilter(django_filters.FilterSet):
    valor_min = django_filters.NumberFilter(field_name="valor", lookup_expr="gte")
    valor_max = django_filters.NumberFilter(field_name="valor", lookup_expr="lte")
    fecha_desde = django_filters.DateFilter(field_name="fecha_cierre_estimada", lookup_expr="gte")
    fecha_hasta = django_filters.DateFilter(field_name="fecha_cierre_estimada", lookup_expr="lte")
    search = django_filters.CharFilter(method="filter_search")
    cliente_id = django_filters.NumberFilter(field_name="cliente_id")
    empresa_id = django_filters.NumberFilter(field_name="empresa_id")

    class Meta:
        model = Oportunidad
        fields = ["estado", "etapa", "moneda"]

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(nombre__icontains=value)


