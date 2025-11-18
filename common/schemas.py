"""Helpers para integrar Pydantic."""

from __future__ import annotations

from typing import Any, Dict, Type

from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import ValidationError


def parse_schema(schema_cls: Type[BaseModel], payload: Dict[str, Any], exclude_unset: bool = False) -> Dict[str, Any]:
    try:
        return schema_cls(**payload).model_dump(mode="json", exclude_unset=exclude_unset)
    except PydanticValidationError as exc:
        raise ValidationError({err["loc"][-1]: [err["msg"]] for err in exc.errors()})



