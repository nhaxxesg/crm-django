from __future__ import annotations

from django.db.models import Count
from drf_spectacular.utils import extend_schema

from common.exceptions import ConstraintError
from common.mixins import CSVExportMixin
from common.viewsets import BaseModelViewSet

from .filters import ClienteFilter
from .models import Cliente
from .schemas import ClienteCreateSchema, ClienteUpdateSchema
from .serializers import ClienteSerializer


@extend_schema(tags=["Clientes"])
class ClienteViewSet(CSVExportMixin, BaseModelViewSet):
    queryset = (
        Cliente.objects.select_related("empresa")
        .annotate(
            num_oportunidades=Count("oportunidades", distinct=True),
            num_actividades=Count("actividades", distinct=True),
        )
    )
    serializer_class = ClienteSerializer
    filterset_class = ClienteFilter
    ordering_fields = ["nombre_completo", "fecha_creacion", "num_oportunidades"]
    list_message = "Clientes obtenidos exitosamente"
    retrieve_message = "Cliente obtenido exitosamente"
    create_message = "Cliente creado exitosamente"
    update_message = "Cliente actualizado exitosamente"
    destroy_message = "Cliente eliminado exitosamente"
    schema_map = {
        "create": ClienteCreateSchema,
        "update": ClienteCreateSchema,
        "partial_update": ClienteUpdateSchema,
    }
    csv_headers = (
        "id",
        "nombre_completo",
        "empresa",
        "telefono",
        "email",
        "num_oportunidades",
        "num_actividades",
        "fecha_creacion",
    )

    def csv_row_builder(self, cliente: Cliente):
        return (
            cliente.id,
            cliente.nombre_completo,
            cliente.empresa.nombre,
            cliente.telefono,
            cliente.email,
            getattr(cliente, "num_oportunidades", 0),
            getattr(cliente, "num_actividades", 0),
            cliente.fecha_creacion.isoformat(),
        )

    def perform_destroy(self, instance: Cliente):
        if instance.oportunidades.filter(estado="abierta").exists():
            raise ConstraintError("No se puede eliminar el cliente con oportunidades activas")
        instance.delete()


