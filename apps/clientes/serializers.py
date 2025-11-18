from __future__ import annotations

from rest_framework import serializers

from apps.empresas.models import Empresa

from .models import Cliente


class EmpresaLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ["id", "nombre"]


class ClienteSerializer(serializers.ModelSerializer):
    empresa = EmpresaLiteSerializer(read_only=True)
    empresa_id = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.all(),
        source="empresa",
    )
    num_oportunidades = serializers.IntegerField(read_only=True)
    num_actividades = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cliente
        fields = [
            "id",
            "nombre_completo",
            "empresa",
            "empresa_id",
            "cargo",
            "telefono",
            "email",
            "direccion",
            "notas",
            "fecha_creacion",
            "num_oportunidades",
            "num_actividades",
        ]
        read_only_fields = ["id", "fecha_creacion", "num_oportunidades", "num_actividades"]


