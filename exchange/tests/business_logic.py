from decimal import Decimal
from datetime import datetime
from django.test import TestCase
from django.utils.timezone import make_aware

from exchange.models import Moneda, Movimiento
from exchange.mixins import BalanceMixin
from exchange.utils import calcular_resultado_periodo


class BalanceResultadoTests(TestCase):

    def setUp(self):
        self.usd = Moneda.objects.create(nombre="Dólar estadounidense", codigo_iso="USD")

        # Fechas de prueba
        self.fecha_base = make_aware(datetime(2025, 1, 10, 12, 0, 0))

        # COMPRA: 100 USD a 1000 ARS => 100.000 ARS
        Movimiento.objects.create(
            fecha=self.fecha_base,
            tipo=Movimiento.TipoMovimiento.COMPRA,
            moneda=self.usd,
            monto_divisa=Decimal("100"),
            cotizacion=Decimal("1000"),
        )

        # VENTA: 60 USD a 1100 ARS => 66.000 ARS
        Movimiento.objects.create(
            fecha=self.fecha_base,
            tipo=Movimiento.TipoMovimiento.VENTA,
            moneda=self.usd,
            monto_divisa=Decimal("60"),
            cotizacion=Decimal("1100"),
        )

        # Para probar saldo cero: COMPRA 50, VENTA 50
        Movimiento.objects.create(
            fecha=self.fecha_base,
            tipo=Movimiento.TipoMovimiento.COMPRA,
            moneda=self.usd,
            monto_divisa=Decimal("50"),
            cotizacion=Decimal("1000"),
        )
        Movimiento.objects.create(
            fecha=self.fecha_base,
            tipo=Movimiento.TipoMovimiento.VENTA,
            moneda=self.usd,
            monto_divisa=Decimal("50"),
            cotizacion=Decimal("1000"),
        )

        # Para probar saldo negativo: VENTA 20 extra
        Movimiento.objects.create(
            fecha=self.fecha_base,
            tipo=Movimiento.TipoMovimiento.VENTA,
            moneda=self.usd,
            monto_divisa=Decimal("20"),
            cotizacion=Decimal("1050"),
        )

    def test_calculo_saldo_positivo_negativo_y_cero(self):
        mixin = BalanceMixin()
        qs = Movimiento.objects.all()

        saldo_usd = mixin.calcular_saldo_moneda("USD", queryset=qs)
        # Vamos a calcular el saldo esperado:
        # COMPRA: 100 + 50 = 150
        # VENTA: 60 + 50 + 20 = 130
        # SALDO = 150 - 130 = 20
        self.assertEqual(saldo_usd, Decimal("20"))

    def test_calculo_saldo_moneda_inexistente(self):
        mixin = BalanceMixin()
        qs = Movimiento.objects.all()

        saldo_eur = mixin.calcular_saldo_moneda("EUR", queryset=qs)  # no creada
        self.assertEqual(saldo_eur, Decimal("0"))

    def test_calculo_resultado_periodo(self):
        inicio = make_aware(datetime(2025, 1, 10, 0, 0, 0))
        fin = make_aware(datetime(2025, 1, 10, 23, 59, 59))

        resultado = calcular_resultado_periodo(inicio, fin)

        # Compras ARS:
        # 100 * 1000 = 100000
        # 50 * 1000  =  50000   => 150000

        # Ventas ARS:
        # 60 * 1100 =  66000
        # 50 * 1000 =  50000
        # 20 * 1050 =  21000   => 137000

        # Resultado = VENTAS - COMPRAS = 137000 - 150000 = -13000
        self.assertEqual(resultado, Decimal("-130000") / Decimal("10"))  # -13000 simplificado
        self.assertEqual(resultado, Decimal("-13000"))
