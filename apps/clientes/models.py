from __future__ import annotations

from django.db import models

from apps.empresas.models import Empresa


class Cliente(models.Model):
    """Contacto asociado a una empresa."""

    nombre_completo = models.CharField(max_length=150)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="clientes")
    cargo = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.CharField(max_length=300, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre_completo"]

    def __str__(self) -> str:
        return f"{self.nombre_completo} - {self.empresa.nombre}"



