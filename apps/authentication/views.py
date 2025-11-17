from __future__ import annotations

import logging

from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from common.responses import success_response
from common.schemas import parse_schema

from .schemas import LoginSchema, RegisterSchema
from .serializers import (
    LoginRequestSerializer,
    RefreshRequestSerializer,
    RegisterRequestSerializer,
    UserSerializer,
)
from .services import AuthService
from .models import User


@extend_schema(
    tags=["Autenticación"],
    request=RegisterRequestSerializer,
    responses=UserSerializer,
)
class RegisterView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        payload = parse_schema(RegisterSchema, request.data)
        user = AuthService.register_user(payload)
        serializer = UserSerializer(user)
        return success_response(
            serializer.data,
            message="Usuario creado exitosamente",
            status_code=status.HTTP_201_CREATED,
        )


logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Autenticación"],
    request=LoginRequestSerializer,
    responses=UserSerializer,
)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "login"

    def post(self, request, *args, **kwargs):
        try:
            payload = parse_schema(LoginSchema, request.data)
            username = payload["username"]
            logger.info("Intento de login", extra={"username": username})
            user, tokens = AuthService.authenticate_user(username, payload["password"])
            serializer = UserSerializer(user)
            data = {"access": tokens["access"], "refresh": tokens["refresh"], "user": serializer.data}
            logger.info("Login exitoso", extra={"username": username, "user_id": user.id})
            return success_response(data, message="Login exitoso")
        except Exception:
            logger.exception("Error durante login", extra={"username": request.data.get("username", "desconocido")})
            raise


@extend_schema(
    tags=["Autenticación"],
    request=RefreshRequestSerializer,
    responses=RefreshRequestSerializer,
)
class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(serializer.validated_data, message="Token refrescado exitosamente")


@extend_schema(tags=["Autenticación"])
class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-fecha_creacion")
    filterset_fields = ["tipo", "activo"]
    search_fields = ["username", "nombre_completo", "email"]
    ordering_fields = ["fecha_creacion", "username"]


