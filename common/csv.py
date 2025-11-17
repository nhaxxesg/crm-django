"""Exportación a CSV."""

from __future__ import annotations

import csv
from io import StringIO
from typing import Iterable, List, Sequence

from django.http import HttpResponse


def render_csv(filename: str, headers: Sequence[str], rows: Iterable[Sequence]):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)

    response = HttpResponse(buffer.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


