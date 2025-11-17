from __future__ import annotations

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nombre_completo",
            "email",
            "tipo",
            "activo",
            "fecha_creacion",
        ]
        read_only_fields = ["id", "fecha_creacion"]



