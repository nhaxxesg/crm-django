from __future__ import annotations

from rest_framework import serializers

from apps.authentication.models import User
from apps.clientes.models import Cliente
from apps.oportunidades.models import Oportunidad

from .models import Actividad


class ClienteLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre_completo"]


class OportunidadLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oportunidad
        fields = ["id", "nombre"]


class UsuarioLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nombre_completo"]


class ActividadSerializer(serializers.ModelSerializer):
    cliente = ClienteLiteSerializer(read_only=True)
    oportunidad = OportunidadLiteSerializer(read_only=True)
    usuario = UsuarioLiteSerializer(read_only=True)

    class Meta:
        model = Actividad
        fields = [
            "id",
            "tipo",
            "asunto",
            "descripcion",
            "fecha_hora",
            "estado",
            "cliente",
            "cliente_id",
            "oportunidad",
            "oportunidad_id",
            "usuario",
            "usuario_id",
            "resultado",
            "fecha_creacion",
        ]
        read_only_fields = ["id", "usuario", "usuario_id", "fecha_creacion"]


