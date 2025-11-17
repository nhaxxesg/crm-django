from __future__ import annotations

from django.db import models


class Empresa(models.Model):
    """Empresa cliente."""

    INDUSTRIAS = [
        ("tecnologia", "Tecnología"),
        ("servicios", "Servicios"),
        ("manufactura", "Manufactura"),
        ("comercio", "Comercio"),
        ("salud", "Salud"),
        ("educacion", "Educación"),
        ("otros", "Otros"),
    ]

    nombre = models.CharField(max_length=200, unique=True)
    industria = models.CharField(max_length=20, choices=INDUSTRIAS, null=True, blank=True)
    num_empleados = models.PositiveIntegerField(null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=300, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre



