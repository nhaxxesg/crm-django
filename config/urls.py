"""URL principal del CRM API."""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.authentication.urls")),
    path("api/v1/empresas/", include("apps.empresas.urls")),
    path("api/v1/clientes/", include("apps.clientes.urls")),
    path("api/v1/oportunidades/", include("apps.oportunidades.urls")),
    path("api/v1/actividades/", include("apps.actividades.urls")),
    path("api/v1/reportes/", include("apps.reportes.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-swagger",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-redoc",
    ),
]



