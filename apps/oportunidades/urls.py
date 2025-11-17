from __future__ import annotations

from rest_framework.routers import DefaultRouter

from .views import OportunidadViewSet

router = DefaultRouter()
router.register("", OportunidadViewSet, basename="oportunidad")

urlpatterns = router.urls


