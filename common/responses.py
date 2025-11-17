"""Helpers para respuestas estandarizadas."""

from __future__ import annotations

from typing import Any, Dict, Optional

from rest_framework.response import Response
from rest_framework import status


def success_response(
    data: Any = None,
    *,
    message: str = "",
    status_code: int = status.HTTP_200_OK,
    **extra: Any,
) -> Response:
    # Patrón Factory para construir payloads consistentes.
    payload: Dict[str, Any] = {"success": True, "data": data, "message": message}
    payload.update(extra)
    return Response(payload, status=status_code)


def error_response(
    code: str,
    message: str,
    *,
    details: Optional[Dict[str, Any]] = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    payload: Dict[str, Any] = {
        "success": False,
        "error": {"code": code, "message": message},
    }
    if details:
        payload["error"]["details"] = details
    return Response(payload, status=status_code)



