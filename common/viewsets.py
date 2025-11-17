"""ViewSets con respuestas estandarizadas."""

from __future__ import annotations

from typing import Any, Dict, Type

from pydantic import BaseModel
from rest_framework import status, viewsets
from rest_framework.response import Response

from .responses import success_response
from .schemas import parse_schema


class SchemaValidationMixin:
    """Aplica el patrón Adapter para reutilizar esquemas Pydantic con DRF."""

    schema_map: Dict[str, Type[BaseModel]] = {}

    def parse_payload(self, request) -> Dict[str, Any]:
        schema_cls = self.schema_map.get(self.action)
        if not schema_cls:
            return request.data
        return parse_schema(schema_cls, request.data)


class BaseModelViewSet(SchemaValidationMixin, viewsets.ModelViewSet):
    list_message = "Listado obtenido exitosamente"
    retrieve_message = "Recurso obtenido exitosamente"
    create_message = "Recurso creado exitosamente"
    update_message = "Recurso actualizado exitosamente"
    destroy_message = "Recurso eliminado exitosamente"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data["message"] = self.list_message
            return response

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            serializer.data,
            count=len(serializer.data),
            message=self.list_message,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data, message=self.retrieve_message)

    def create(self, request, *args, **kwargs):
        data = self.parse_payload(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(
            serializer.data,
            message=self.create_message,
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        data = self.parse_payload(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response(serializer.data, message=self.update_message)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(message=self.destroy_message)


