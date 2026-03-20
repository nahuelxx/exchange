from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError


class Moneda(models.Model):

    nombre = models.CharField(max_length=50)
    codigo_iso = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"
        ordering = ["codigo_iso"]

    def __str__(self) -> str:
        return f"{self.codigo_iso}"


class Movimiento(models.Model):
    class TipoMovimiento(models.TextChoices):
        COMPRA = "compra", "Compra"
        VENTA = "venta", "Venta"

    fecha = models.DateTimeField()

    tipo = models.CharField(
        max_length=10,
        choices=TipoMovimiento.choices,
    )
    moneda = models.ForeignKey(
        Moneda,
        on_delete=models.PROTECT,
        related_name="movimientos",
    )

    monto_divisa = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    cotizacion = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        help_text="Cotización de la divisa expresada en ARS.",
    )

    total_ars = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="monto_divisa * cotizacion. Se calcula automáticamente.",
    )


    fuente = models.CharField(
        max_length=50,
        blank=True,
        help_text="Origen del movimiento: Liu, cliente, caja, etc.",
    )

    notas = models.TextField(
        blank=True,
        help_text="Campo libre para observaciones.",
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """
        Invariantes:
        - monto_divisa > 0
        - cotizacion > 0
        - total_ars se calcula automáticamente como monto_divisa * cotizacion
        """
        super().clean()

        if self.monto_divisa is None or self.monto_divisa <= 0:
            raise ValidationError({"monto_divisa": "El monto de la divisa debe ser mayor a cero."})

        if self.cotizacion is None or self.cotizacion <= 0:
            raise ValidationError({"cotizacion": "La cotización debe ser mayor a cero."})

        # Calcular total_ars de forma consistente
        self.total_ars = (self.monto_divisa * self.cotizacion).quantize(Decimal("0.01"))

    def save(self, *args, **kwargs):
        # Aseguramos que clean() se ejecute siempre antes de guardar
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ["-fecha", "-creado"]

    def __str__(self) -> str:
        return (
            f"{self.fecha:%Y-%m-%d %H:%M} - "
            f"{self.get_tipo_display()} "
            f"{self.monto_divisa} {self.moneda.codigo_iso}"
        )



