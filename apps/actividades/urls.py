from __future__ import annotations

from rest_framework.routers import DefaultRouter

from .views import ActividadViewSet

router = DefaultRouter()
router.register("", ActividadViewSet, basename="actividad")

urlpatterns = router.urls


