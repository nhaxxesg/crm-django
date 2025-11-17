from __future__ import annotations

from django.urls import path

from .views import (
    ClientesPorEmpresaView,
    ConversionReportView,
    DashboardView,
    VentasReportView,
)

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("ventas/", VentasReportView.as_view(), name="reporte-ventas"),
    path("conversion/", ConversionReportView.as_view(), name="reporte-conversion"),
    path(
        "clientes-por-empresa/",
        ClientesPorEmpresaView.as_view(),
        name="clientes-por-empresa",
    ),
]


