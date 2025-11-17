"""Filtros de logging."""

from __future__ import annotations

import logging
from uuid import uuid4


class RequestIDFilter(logging.Filter):
    """Genera un identificador corto por evento."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = uuid4().hex[:8]
        return True



