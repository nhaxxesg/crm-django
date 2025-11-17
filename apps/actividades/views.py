from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from common.mixins import CSVExportMixin
from common.responses import success_response
from common.viewsets import BaseModelViewSet

from .filters import ActividadFilter
from .models import Actividad
from .schemas import ActividadCompletarSchema, ActividadCreateSchema, ActividadUpdateSchema
from .serializers import ActividadSerializer


@extend_schema(tags=["Actividades"])
class ActividadViewSet(CSVExportMixin, BaseModelViewSet):
    queryset = Actividad.objects.select_related("cliente", "oportunidad", "usuario")
    serializer_class = ActividadSerializer
    filterset_class = ActividadFilter
    ordering_fields = ["fecha_hora", "fecha_creacion"]
    list_message = "Actividades obtenidas exitosamente"
    retrieve_message = "Actividad obtenida exitosamente"
    create_message = "Actividad creada exitosamente"
    update_message = "Actividad actualizada exitosamente"
    destroy_message = "Actividad eliminada exitosamente"
    schema_map = {
        "create": ActividadCreateSchema,
        "update": ActividadCreateSchema,
        "partial_update": ActividadUpdateSchema,
        "completar": ActividadCompletarSchema,
    }
    csv_headers = (
        "id",
        "tipo",
        "asunto",
        "estado",
        "cliente",
        "oportunidad",
        "usuario",
        "fecha_hora",
    )

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def csv_row_builder(self, actividad: Actividad):
        return (
            actividad.id,
            actividad.tipo,
            actividad.asunto,
            actividad.estado,
            actividad.cliente.nombre_completo if actividad.cliente else "",
            actividad.oportunidad.nombre if actividad.oportunidad else "",
            actividad.usuario.nombre_completo,
            actividad.fecha_hora.isoformat(),
        )

    @action(detail=True, methods=["patch"], url_path="completar")
    def completar(self, request, *args, **kwargs):
        payload = self.parse_payload(request)
        actividad = self.get_object()
        actividad.estado = "completada"
        actividad.resultado = payload["resultado"]
        actividad.save(update_fields=["estado", "resultado"])
        serializer = self.get_serializer(actividad)
        return success_response(serializer.data, message="Actividad marcada como completada")


