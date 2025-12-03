from decimal import Decimal
from typing import Optional

from django.db.models import Sum, models

from .models import Movimiento


def calcular_resultado_periodo(
    fecha_inicio,
    fecha_fin,
    queryset: Optional["models.QuerySet"] = None,
) -> Decimal:
    """
    Calcula el resultado (ganancia/pérdida) en ARS para un rango de fechas.

    resultado = sum(total_ars de VENTAS) - sum(total_ars de COMPRAS)

    :param fecha_inicio: datetime (inclusive)
    :param fecha_fin: datetime (inclusive o exclusivo, según diseño)
    :param queryset: queryset opcional de Movimiento para filtrar adicionalmente.
    :return: Decimal con resultado en ARS (positivo = ganancia, negativo = pérdida).
    """
    if queryset is None:
        queryset = Movimiento.objects.all()

    qs = queryset.filter(
        fecha__gte=fecha_inicio,
        fecha__lte=fecha_fin,
    )

    compras_ars = qs.filter(tipo=Movimiento.TipoMovimiento.COMPRA).aggregate(
        total=Sum("total_ars")
    )["total"] or Decimal("0")

    ventas_ars = qs.filter(tipo=Movimiento.TipoMovimiento.VENTA).aggregate(
        total=Sum("total_ars")
    )["total"] or Decimal("0")

    return ventas_ars - compras_ars
