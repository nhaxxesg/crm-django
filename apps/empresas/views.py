from __future__ import annotations

from django.db.models import Count

from common.exceptions import ConstraintError
from common.mixins import CSVExportMixin
from common.viewsets import BaseModelViewSet

from .filters import EmpresaFilter
from .models import Empresa
from .schemas import EmpresaCreateSchema, EmpresaUpdateSchema
from .serializers import EmpresaDetailSerializer, EmpresaSerializer


class EmpresaViewSet(CSVExportMixin, BaseModelViewSet):
    queryset = (
        Empresa.objects.all()
        .annotate(
            num_clientes=Count("clientes", distinct=True),
            num_oportunidades=Count("oportunidades", distinct=True),
        )
        .prefetch_related("clientes", "oportunidades")
    )
    serializer_class = EmpresaSerializer
    filterset_class = EmpresaFilter
    ordering_fields = ["nombre", "fecha_creacion", "num_clientes", "num_oportunidades"]
    list_message = "Empresas obtenidas exitosamente"
    retrieve_message = "Empresa obtenida exitosamente"
    create_message = "Empresa creada exitosamente"
    update_message = "Empresa actualizada exitosamente"
    destroy_message = "Empresa eliminada exitosamente"
    schema_map = {
        "create": EmpresaCreateSchema,
        "update": EmpresaCreateSchema,
        "partial_update": EmpresaUpdateSchema,
    }
    csv_headers = (
        "id",
        "nombre",
        "industria",
        "num_empleados",
        "telefono",
        "num_clientes",
        "num_oportunidades",
        "fecha_creacion",
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EmpresaDetailSerializer
        return super().get_serializer_class()

    def csv_row_builder(self, empresa: Empresa):
        return (
            empresa.id,
            empresa.nombre,
            empresa.industria or "",
            empresa.num_empleados or "",
            empresa.telefono or "",
            getattr(empresa, "num_clientes", 0),
            getattr(empresa, "num_oportunidades", 0),
            empresa.fecha_creacion.isoformat(),
        )

    def perform_destroy(self, instance: Empresa):
        if instance.clientes.exists() or instance.oportunidades.exists():
            raise ConstraintError(
                "No se puede eliminar la empresa porque tiene clientes u oportunidades asociadas"
            )
        instance.delete()


