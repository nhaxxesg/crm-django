"""Manejo de errores centralizado."""

from __future__ import annotations

from typing import Any, Dict

from pydantic import ValidationError as PydanticValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from .responses import error_response


class ConstraintError(APIException):
    """Señala violaciones de integridad referencial."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = "No se puede completar la operación por restricciones de integridad"
    default_code = "constraint_error"


def format_pydantic_errors(exc: PydanticValidationError) -> Dict[str, Any]:
    errors: Dict[str, Any] = {}
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"])
        errors.setdefault(field, []).append(err["msg"])
    return errors


def drf_exception_handler(exc: Exception, context: Dict[str, Any]):
    response = exception_handler(exc, context)

    if isinstance(exc, PydanticValidationError):
        return error_response(
            code="VALIDATION_ERROR",
            message="Los datos proporcionados no son válidos",
            details=format_pydantic_errors(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, APIException) and response is not None:
        code = getattr(exc, "default_code", "error").upper()
        message = getattr(exc, "default_detail", "Error")
        details = response.data if isinstance(response.data, dict) else {"detail": response.data}
        return error_response(
            code=code,
            message=str(message),
            details=details,
            status_code=response.status_code,
        )

    if response is None:
        return error_response(
            code="SERVER_ERROR",
            message="Ocurrió un error inesperado",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response



