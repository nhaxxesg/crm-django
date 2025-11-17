from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.clientes.models import Cliente
from apps.oportunidades.models import Oportunidad


class Actividad(models.Model):
    """Registro de actividades."""

    TIPOS = [
        ("llamada", "Llamada"),
        ("reunion", "Reunión"),
        ("email", "Email"),
        ("tarea", "Tarea"),
    ]

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("completada", "Completada"),
        ("cancelada", "Cancelada"),
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default="pendiente")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="actividades", null=True, blank=True)
    oportunidad = models.ForeignKey(Oportunidad, on_delete=models.CASCADE, related_name="actividades", null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actividades")
    resultado = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_hora"]

    def __str__(self) -> str:
        return f"{self.asunto} - {self.estado}"



