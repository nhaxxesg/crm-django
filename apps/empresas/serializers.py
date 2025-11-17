from __future__ import annotations

from rest_framework import serializers

from apps.clientes.models import Cliente
from apps.oportunidades.models import Oportunidad

from .models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    num_clientes = serializers.IntegerField(read_only=True)
    num_oportunidades = serializers.IntegerField(read_only=True)

    class Meta:
        model = Empresa
        fields = [
            "id",
            "nombre",
            "industria",
            "num_empleados",
            "sitio_web",
            "telefono",
            "direccion",
            "notas",
            "fecha_creacion",
            "num_clientes",
            "num_oportunidades",
        ]
        read_only_fields = ["id", "fecha_creacion", "num_clientes", "num_oportunidades"]


class ClienteResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre_completo", "cargo", "email"]


class OportunidadResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oportunidad
        fields = ["id", "nombre", "valor", "etapa"]


class EmpresaDetailSerializer(EmpresaSerializer):
    clientes = ClienteResumenSerializer(many=True, read_only=True)
    oportunidades = OportunidadResumenSerializer(many=True, read_only=True)

    class Meta(EmpresaSerializer.Meta):
        fields = EmpresaSerializer.Meta.fields + ["clientes", "oportunidades"]



