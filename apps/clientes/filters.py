from __future__ import annotations

from django.db import models
import django_filters

from .models import Cliente


class ClienteFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    empresa_id = django_filters.NumberFilter(field_name="empresa_id")

    class Meta:
        model = Cliente
        fields = []

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            models.Q(nombre_completo__icontains=value)
            | models.Q(email__icontains=value)
        )


