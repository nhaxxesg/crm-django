from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, List

from django.db.models import Avg, Count, DecimalField, DurationField, ExpressionWrapper, F, Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek
from django.utils import timezone

from apps.actividades.models import Actividad
from apps.clientes.models import Cliente
from apps.empresas.models import Empresa
from apps.oportunidades.models import Oportunidad


class ReporteService:
    """Service Layer para mantener las agregaciones desacopladas de las vistas."""

    @staticmethod
    def dashboard() -> Dict[str, object]:
        clientes = Cliente.objects.count()
        empresas = Empresa.objects.count()
        oportunidades_abiertas = Oportunidad.objects.filter(estado="abierta").count()
        oportunidades_cerradas = Oportunidad.objects.filter(estado="cerrada").count()
        actividades_pendientes = Actividad.objects.filter(estado="pendiente").count()
        actividades_completadas = Actividad.objects.filter(estado="completada").count()

        abiertas = Oportunidad.objects.filter(estado="abierta")
        valores = abiertas.aggregate(
            valor_total=Sum("valor"),
            valor_ponderado=Sum(
                ExpressionWrapper(
                    F("valor") * F("probabilidad") / 100,
                    output_field=DecimalField(max_digits=14, decimal_places=2),
                )
            ),
        )

        now = timezone.now().date()
        mes_actual_inicio = now.replace(day=1)
        mes_anterior_fin = mes_actual_inicio - timedelta(days=1)
        mes_anterior_inicio = mes_anterior_fin.replace(day=1)

        ventas_actual = ReporteService._ventas_por_rango(mes_actual_inicio, now)
        ventas_anterior = ReporteService._ventas_por_rango(mes_anterior_inicio, mes_anterior_fin)

        etapas = {
            etapa: Oportunidad.objects.filter(etapa=etapa).count()
            for etapa, _ in Oportunidad.ETAPAS
        }
        actividades_tipo = {
            tipo: Actividad.objects.filter(tipo=tipo).count()
            for tipo, _ in Actividad.TIPOS
        }

        return {
            "totales": {
                "clientes": clientes,
                "empresas": empresas,
                "oportunidades_abiertas": oportunidades_abiertas,
                "oportunidades_cerradas": oportunidades_cerradas,
                "actividades_pendientes": actividades_pendientes,
                "actividades_completadas": actividades_completadas,
            },
            "valores": {
                "valor_total_pipeline": float(valores["valor_total"] or 0),
                "valor_ponderado_pipeline": float(valores["valor_ponderado"] or 0),
                "ventas_cerradas_mes_actual": ventas_actual,
                "ventas_cerradas_mes_anterior": ventas_anterior,
            },
            "oportunidades_por_etapa": etapas,
            "actividades_por_tipo": actividades_tipo,
        }

    @staticmethod
    def reporte_ventas(
        fecha_inicio: date, fecha_fin: date, agrupar_por: str, moneda: str | None
    ) -> Dict[str, object]:
        queryset = Oportunidad.objects.filter(
            estado="cerrada",
            resultado="ganada",
            fecha_cierre_real__date__gte=fecha_inicio,
            fecha_cierre_real__date__lte=fecha_fin,
        )
        if moneda:
            queryset = queryset.filter(moneda=moneda)

        total_ventas = queryset.count()
        valor_total = queryset.aggregate(total=Sum("valor"))["total"] or Decimal("0")
        ticket_promedio = float(valor_total / total_ventas) if total_ventas else 0.0

        trunc_map = {"dia": TruncDay, "semana": TruncWeek, "mes": TruncMonth}
        trunc = trunc_map[agrupar_por]

        ventas_por_periodo: List[Dict[str, object]] = []
        for item in (
            queryset.annotate(periodo=trunc("fecha_cierre_real"))
            .values("periodo")
            .annotate(cantidad=Count("id"), valor_total=Sum("valor"))
            .order_by("periodo")
        ):
            periodo_dt = item["periodo"]
            if agrupar_por == "mes":
                periodo_label = periodo_dt.strftime("%Y-%m")
            elif agrupar_por == "semana":
                periodo_label = periodo_dt.strftime("%Y-W%U")
            else:
                periodo_label = periodo_dt.strftime("%Y-%m-%d")
            ventas_por_periodo.append(
                {
                    "periodo": periodo_label,
                    "cantidad": item["cantidad"],
                    "valor_total": float(item["valor_total"] or 0),
                }
            )

        return {
            "periodo": {
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat(),
            },
            "resumen": {
                "total_ventas": total_ventas,
                "valor_total": float(valor_total),
                "ticket_promedio": ticket_promedio,
            },
            "ventas_por_periodo": ventas_por_periodo,
        }

    @staticmethod
    def reporte_conversion() -> Dict[str, object]:
        queryset = Oportunidad.objects.all()
        total_creadas = queryset.count()
        total_ganadas = queryset.filter(resultado="ganada").count()
        total_perdidas = queryset.filter(resultado="perdida").count()

        conversion_general = (
            round((total_ganadas / total_creadas) * 100, 2) if total_creadas else 0.0
        )

        etapas_count = {
            etapa: queryset.filter(etapa=etapa).count()
            for etapa, _ in Oportunidad.ETAPAS
        }

        def ratio(numerador: int, denominador: int) -> float:
            return round((numerador / denominador) * 100, 2) if denominador else 0.0

        conversion_por_etapa = {
            "prospeccion_a_calificacion": ratio(
                etapas_count.get("calificacion", 0), etapas_count.get("prospeccion", 0)
            ),
            "calificacion_a_propuesta": ratio(
                etapas_count.get("propuesta", 0), etapas_count.get("calificacion", 0)
            ),
            "propuesta_a_negociacion": ratio(
                etapas_count.get("negociacion", 0), etapas_count.get("propuesta", 0)
            ),
            "negociacion_a_cierre": ratio(
                queryset.filter(etapa__in=["cerrado_ganado", "cerrado_perdido"]).count(),
                etapas_count.get("negociacion", 0),
            ),
        }

        duracion = (
            queryset.filter(fecha_cierre_real__isnull=False)
            .annotate(
                duracion=ExpressionWrapper(
                    F("fecha_cierre_real") - F("fecha_creacion"),
                    output_field=DurationField(),
                )
            )
            .aggregate(promedio=Avg("duracion"))
        )
        promedio = duracion["promedio"]
        tiempo_promedio_dias = int(promedio.total_seconds() // 86400) if promedio else 0

        return {
            "total_oportunidades_creadas": total_creadas,
            "total_cerradas_ganadas": total_ganadas,
            "total_cerradas_perdidas": total_perdidas,
            "tasa_conversion_general": conversion_general,
            "conversion_por_etapa": conversion_por_etapa,
            "tiempo_promedio_cierre_dias": tiempo_promedio_dias,
        }

    @staticmethod
    def clientes_por_empresa() -> List[Dict[str, object]]:
        empresas = (
            Empresa.objects.annotate(
                num_clientes=Count("clientes", distinct=True),
                num_oportunidades=Count("oportunidades", distinct=True),
                valor_total=Sum("oportunidades__valor"),
            )
            .order_by("nombre")
            .values(
                "id",
                "nombre",
                "num_clientes",
                "num_oportunidades",
                "valor_total",
            )
        )

        return [
            {
                "empresa_id": item["id"],
                "empresa_nombre": item["nombre"],
                "num_clientes": item["num_clientes"],
                "num_oportunidades": item["num_oportunidades"],
                "valor_total_oportunidades": float(item["valor_total"] or 0),
            }
            for item in empresas
        ]

    @staticmethod
    def _ventas_por_rango(fecha_inicio: date, fecha_fin: date) -> float:
        total = (
            Oportunidad.objects.filter(
                estado="cerrada",
                resultado="ganada",
                fecha_cierre_real__date__gte=fecha_inicio,
                fecha_cierre_real__date__lte=fecha_fin,
            ).aggregate(total=Sum("valor"))["total"]
            or 0
        )
        return float(total)


