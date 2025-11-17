from __future__ import annotations

from rest_framework import serializers

from apps.clientes.models import Cliente
from apps.empresas.models import Empresa

from .models import Oportunidad


class ClienteLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre_completo", "email"]


class EmpresaLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ["id", "nombre"]


class OportunidadSerializer(serializers.ModelSerializer):
    cliente = ClienteLiteSerializer(read_only=True)
    empresa = EmpresaLiteSerializer(read_only=True)
    valor_ponderado = serializers.SerializerMethodField()

    class Meta:
        model = Oportunidad
        fields = [
            "id",
            "nombre",
            "cliente",
            "cliente_id",
            "empresa",
            "empresa_id",
            "valor",
            "moneda",
            "probabilidad",
            "valor_ponderado",
            "fecha_cierre_estimada",
            "etapa",
            "estado",
            "resultado",
            "notas",
            "fecha_creacion",
            "fecha_cierre_real",
        ]
        read_only_fields = [
            "id",
            "valor_ponderado",
            "fecha_creacion",
            "fecha_cierre_real",
        ]

    def get_valor_ponderado(self, obj: Oportunidad) -> float:
        return obj.valor_ponderado


