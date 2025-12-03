from decimal import Decimal

from django.db.models import Sum, F
from django.utils import timezone


class BalanceMixin:
    """
    Mixin reutilizable para calcular saldos por moneda.

    Se puede usar con:
    - ViewSets (llamando self.get_queryset())
    - Managers (usando self.get_queryset())
    - Scripts standalone (pasando un queryset manualmente)
    """

    def get_base_queryset(self):
        """
        Si el mixin se usa en un View o Manager que
        define get_queryset(), lo respetamos.
        Caso contrario, debe ser overrideado o se
        le pasará un queryset explícito a las funciones.
        """
        if hasattr(self, "get_queryset"):
            return self.get_queryset()
        return None

    def calcular_saldo_moneda(self, moneda, queryset=None):
        """
        Calcula el saldo actual de una moneda específica.

        saldo = sum(compras) - sum(ventas)

        :param moneda: instancia de Moneda o su código ISO (string)
        :param queryset: queryset opcional de Movimiento; si no se pasa,
                         intenta usar self.get_queryset().
        :return: Decimal con el saldo en unidades de la divisa.
        """
        from .models import Movimiento, Moneda  # import local para evitar ciclos

        if queryset is None:
            queryset = self.get_base_queryset()
        if queryset is None:
            queryset = Movimiento.objects.all()

        if isinstance(moneda, str):
            moneda_obj = Moneda.objects.filter(codigo_iso=moneda).first()
        else:
            moneda_obj = moneda

        if moneda_obj is None:
            return Decimal("0")

        qs = queryset.filter(moneda=moneda_obj)

        compras = qs.filter(tipo=Movimiento.TipoMovimiento.COMPRA).aggregate(
            total=Sum("monto_divisa")
        )["total"] or Decimal("0")

        ventas = qs.filter(tipo=Movimiento.TipoMovimiento.VENTA).aggregate(
            total=Sum("monto_divisa")
        )["total"] or Decimal("0")

        return compras - ventas
