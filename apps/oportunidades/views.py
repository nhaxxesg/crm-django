from __future__ import annotations

from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from rest_framework.decorators import action

from common.mixins import CSVExportMixin
from common.responses import success_response
from common.viewsets import BaseModelViewSet

from .filters import OportunidadFilter
from .models import Oportunidad
from .schemas import ActualizarEtapaSchema, OportunidadCreateSchema, OportunidadUpdateSchema
from .serializers import OportunidadSerializer
from .services import OportunidadService


class OportunidadViewSet(CSVExportMixin, BaseModelViewSet):
    queryset = Oportunidad.objects.select_related("cliente", "cliente__empresa", "empresa")
    serializer_class = OportunidadSerializer
    filterset_class = OportunidadFilter
    ordering_fields = ["valor", "probabilidad", "fecha_creacion", "fecha_cierre_estimada"]
    list_message = "Oportunidades obtenidas exitosamente"
    retrieve_message = "Oportunidad obtenida exitosamente"
    create_message = "Oportunidad creada exitosamente"
    update_message = "Oportunidad actualizada exitosamente"
    destroy_message = "Oportunidad eliminada exitosamente"
    schema_map = {
        "create": OportunidadCreateSchema,
        "update": OportunidadCreateSchema,
        "partial_update": OportunidadUpdateSchema,
        "actualizar_etapa": ActualizarEtapaSchema,
    }
    csv_headers = (
        "id",
        "nombre",
        "cliente",
        "empresa",
        "valor",
        "moneda",
        "probabilidad",
        "etapa",
        "estado",
        "fecha_cierre_estimada",
        "fecha_creacion",
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        totals = queryset.aggregate(
            total_valor=Sum("valor"),
            total_valor_ponderado=Sum(
                ExpressionWrapper(
                    F("valor") * F("probabilidad") / 100,
                    output_field=DecimalField(max_digits=14, decimal_places=2),
                )
            ),
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response = success_response(
                serializer.data,
                count=len(serializer.data),
                message=self.list_message,
            )
        response.data["total_valor"] = float(totals["total_valor"] or 0)
        response.data["total_valor_ponderado"] = float(totals["total_valor_ponderado"] or 0)
        return response

    def csv_row_builder(self, oportunidad: Oportunidad):
        return (
            oportunidad.id,
            oportunidad.nombre,
            oportunidad.cliente.nombre_completo,
            oportunidad.empresa.nombre,
            float(oportunidad.valor),
            oportunidad.moneda,
            oportunidad.probabilidad,
            oportunidad.etapa,
            oportunidad.estado,
            oportunidad.fecha_cierre_estimada.isoformat(),
            oportunidad.fecha_creacion.isoformat(),
        )

    @action(detail=False, methods=["get"], url_path="pipeline")
    def pipeline(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data, total_count, total_valor = OportunidadService.build_pipeline(queryset, OportunidadSerializer)
        return success_response(
            data,
            message="Pipeline obtenido exitosamente",
            total_oportunidades=total_count,
            total_valor=total_valor,
        )

    @action(detail=True, methods=["patch"], url_path="actualizar-etapa")
    def actualizar_etapa(self, request, *args, **kwargs):
        payload = self.parse_payload(request)
        oportunidad = self.get_object()
        oportunidad = OportunidadService.actualizar_etapa(
            oportunidad,
            payload["etapa"],
            payload.get("notas"),
        )
        serializer = self.get_serializer(oportunidad)
        return success_response(serializer.data, message="Etapa actualizada exitosamente")


