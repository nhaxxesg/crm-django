"""Mixins reutilizables."""

from __future__ import annotations

from typing import Iterable, Sequence

from rest_framework.decorators import action
from rest_framework.response import Response

from .csv import render_csv


class CSVExportMixin:
    csv_headers: Sequence[str] = ()
    csv_row_builder = None

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        rows = (
            self.csv_row_builder(item) if self.csv_row_builder else ()
            for item in queryset
        )
        base_name = getattr(self, "basename", self.__class__.__name__.lower())
        filename = f"{base_name}.csv"
        return render_csv(filename, self.csv_headers, rows)


