from datetime import datetime, time
from decimal import Decimal
from django.db.models import Sum
from django.utils.timezone import make_aware, is_naive

from exchange.models import Movimiento, Moneda


def _to_dt_range(fecha_str: str):
    """
    Convierte YYYY-MM-DD en rango datetime del día completo.
    """
    d = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    start = datetime.combine(d, time.min)
    end = datetime.combine(d, time.max)

    if is_naive(start):
        start = make_aware(start)
    if is_naive(end):
        end = make_aware(end)

    return start, end


def build_daily_stats(fecha_str: str):
    """
    Genera estadísticas diarias para una fecha dada (YYYY-MM-DD).
    Devuelve un dict listo para Response(JSON) o para IA.
    """
    start, end = _to_dt_range(fecha_str)

    qs = Movimiento.objects.filter(
        fecha__range=(start, end)
    ).select_related("moneda").order_by("-fecha", "-creado")

    compras_ars = qs.filter(
        tipo=Movimiento.TipoMovimiento.COMPRA
    ).aggregate(total=Sum("total_ars"))["total"] or Decimal("0")

    ventas_ars = qs.filter(
        tipo=Movimiento.TipoMovimiento.VENTA
    ).aggregate(total=Sum("total_ars"))["total"] or Decimal("0")

    resultado_ars = ventas_ars - compras_ars

    por_moneda_del_dia = {}

    for moneda in Moneda.objects.all().order_by("codigo_iso"):
        compras_divisa = qs.filter(
            moneda=moneda,
            tipo=Movimiento.TipoMovimiento.COMPRA
        ).aggregate(total=Sum("monto_divisa"))["total"] or Decimal("0")

        ventas_divisa = qs.filter(
            moneda=moneda,
            tipo=Movimiento.TipoMovimiento.VENTA
        ).aggregate(total=Sum("monto_divisa"))["total"] or Decimal("0")

        saldo_dia_divisa = compras_divisa - ventas_divisa

        por_moneda_del_dia[moneda.codigo_iso] = {
            "compras_divisa": str(compras_divisa),
            "ventas_divisa": str(ventas_divisa),
            "saldo_dia_divisa": str(saldo_dia_divisa),
        }

    # saldo global acumulado por moneda
    saldos_actuales = {}

    for moneda in Moneda.objects.all().order_by("codigo_iso"):
        compras_total = Movimiento.objects.filter(
            moneda=moneda,
            tipo=Movimiento.TipoMovimiento.COMPRA
        ).aggregate(total=Sum("monto_divisa"))["total"] or Decimal("0")

        ventas_total = Movimiento.objects.filter(
            moneda=moneda,
            tipo=Movimiento.TipoMovimiento.VENTA
        ).aggregate(total=Sum("monto_divisa"))["total"] or Decimal("0")

        saldos_actuales[moneda.codigo_iso] = str(compras_total - ventas_total)

    movimientos_del_dia = []
    for mov in qs:
        movimientos_del_dia.append({
            "id": mov.id,
            "fecha": mov.fecha.isoformat(),
            "tipo": mov.tipo,
            "moneda": mov.moneda.id,
            "moneda_codigo": mov.moneda.codigo_iso,
            "monto_divisa": str(mov.monto_divisa),
            "cotizacion": str(mov.cotizacion),
            "total_ars": str(mov.total_ars),
            "fuente": mov.fuente,
            "notas": mov.notas,
            "creado": mov.creado.isoformat(),
            "actualizado": mov.actualizado.isoformat(),
        })

    return {
        "meta": {
            "target_date": fecha_str,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        },
        "kpis": {
            "total_compras_ars": str(compras_ars),
            "total_ventas_ars": str(ventas_ars),
            "resultado_neto_ars": str(resultado_ars),
            "cantidad_movimientos": qs.count(),
        },
        "por_moneda_del_dia": por_moneda_del_dia,
        "saldos_actuales": saldos_actuales,
        "movimientos_del_dia": movimientos_del_dia,
    }