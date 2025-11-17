from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.responses import success_response
from common.schemas import parse_schema

from .schemas import VentasQuerySchema
from .services import ReporteService


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = ReporteService.dashboard()
        return success_response(data, message="Dashboard obtenido exitosamente")


class VentasReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payload = parse_schema(VentasQuerySchema, request.query_params.dict())
        data = ReporteService.reporte_ventas(
            fecha_inicio=payload["fecha_inicio"],
            fecha_fin=payload["fecha_fin"],
            agrupar_por=payload["agrupar_por"],
            moneda=payload.get("moneda"),
        )
        return success_response(data, message="Reporte de ventas generado exitosamente")


class ConversionReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = ReporteService.reporte_conversion()
        return success_response(data, message="Reporte de conversión generado exitosamente")


class ClientesPorEmpresaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = ReporteService.clientes_por_empresa()
        return success_response(data, message="Reporte generado exitosamente")


