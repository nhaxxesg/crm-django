from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.clientes.models import Cliente
from apps.empresas.models import Empresa


class Oportunidad(models.Model):
    """Oportunidades comerciales."""

    ETAPAS = [
        ("prospeccion", "Prospección"),
        ("calificacion", "Calificación"),
        ("propuesta", "Propuesta"),
        ("negociacion", "Negociación"),
        ("cerrado_ganado", "Cerrado Ganado"),
        ("cerrado_perdido", "Cerrado Perdido"),
    ]

    ESTADOS = [("abierta", "Abierta"), ("cerrada", "Cerrada")]
    RESULTADOS = [("ganada", "Ganada"), ("perdida", "Perdida")]

    nombre = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="oportunidades")
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="oportunidades")
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=3, default="PEN")
    probabilidad = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_cierre_estimada = models.DateField()
    etapa = models.CharField(max_length=20, choices=ETAPAS)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="abierta")
    resultado = models.CharField(max_length=10, choices=RESULTADOS, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre_real = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    @property
    def valor_ponderado(self):
        return float(self.valor) * (self.probabilidad / 100)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.etapa})"



