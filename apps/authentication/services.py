"""Servicios de autenticación."""

from __future__ import annotations

from typing import Tuple

from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError, transaction
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthService:
    # Patrón Service Layer para encapsular reglas de negocio reutilizables.
    @staticmethod
    def register_user(data: dict) -> User:
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=data["username"],
                    email=data["email"],
                    password=data["password"],
                    nombre_completo=data["nombre_completo"],
                    tipo=data["tipo"],
                )
                return user
        except IntegrityError as exc:
            raise exceptions.ValidationError(
                {"detail": "El username o email ya existe"}
            ) from exc

    @staticmethod
    def authenticate_user(username: str, password: str) -> Tuple[User, dict]:
        user = authenticate(username=username, password=password)
        if not user:
            raise exceptions.AuthenticationFailed("Usuario o contraseña incorrectos")
        if not user.activo:
            raise exceptions.PermissionDenied("Usuario desactivado")

        refresh = RefreshToken.for_user(user)
        tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
        return user, tokens



