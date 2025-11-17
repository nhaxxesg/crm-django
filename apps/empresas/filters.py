from __future__ import annotations

import django_filters

from .models import Empresa


class EmpresaFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Empresa
        fields = ["industria"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(nombre__icontains=value)


