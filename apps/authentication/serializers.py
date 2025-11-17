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


class RegisterRequestSerializer(serializers.Serializer):
    nombre_completo = serializers.CharField(min_length=3, max_length=100)
    username = serializers.CharField(min_length=3, max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    password_confirm = serializers.CharField(min_length=6)
    tipo = serializers.ChoiceField(choices=["admin", "regular"])


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()



