from django.contrib import admin
from .models import Moneda, Movimiento


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ("codigo_iso", "nombre")
    search_fields = ("codigo_iso", "nombre")


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = (
        "fecha", "tipo", "moneda",
        "monto_divisa", "cotizacion",
        "total_ars", "fuente"
    )
    list_filter = ("tipo", "moneda", "fecha")
    search_fields = ("fuente", "notas")
    date_hierarchy = "fecha"


# Register your models here.
