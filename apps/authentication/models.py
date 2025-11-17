from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuario extendido con rol y estado."""

    ADMIN = "admin"
    REGULAR = "regular"
    TIPOS = [
        (ADMIN, "Administrador"),
        (REGULAR, "Regular"),
    ]

    nombre_completo = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=10, choices=TIPOS, default=REGULAR)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.username} ({self.tipo})"



