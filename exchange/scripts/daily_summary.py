import os
import json
from datetime import datetime, timedelta, time
from decimal import Decimal
from typing import Dict, Any, List
import requests


API_BASE = os.getenv("EXCHANGE_API_BASE", "http://127.0.0.1:8000")
TIMEZONE_NOTE = "El backend usa timezone del servidor. Este script filtra por fecha local en formato YYYY-MM-DD sobre fecha ISO."

def _to_decimal(v) -> Decimal:
    if v is None:
        return Decimal("0")
    return Decimal(str(v))

def _iso_date_prefix(dt_str: str) -> str:
    # dt_str: "2026-01-09T16:34:00-03:00" o "2026-01-09T16:34:00"
    return dt_str[:10]

def fetch_all_movimientos() -> List[Dict[str, Any]]:
    url = f"{API_BASE}/api/movimientos/"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_saldos_actuales() -> Dict[str, str]:
    url = f"{API_BASE}/api/saldos/"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()

def build_daily_summary(target_date: str) -> Dict[str, Any]:
    """
    target_date: 'YYYY-MM-DD' (día a resumir)
    """
    movimientos = fetch_all_movimientos()

    # Filtrar movimientos del día
    day_moves = [m for m in movimientos if _iso_date_prefix(m["fecha"]) == target_date]

    # Totales en ARS
    compras_ars = sum((_to_decimal(m["total_ars"]) for m in day_moves if m["tipo"] == "compra"), Decimal("0"))
    ventas_ars = sum((_to_decimal(m["total_ars"]) for m in day_moves if m["tipo"] == "venta"), Decimal("0"))
    resultado_ars = ventas_ars - compras_ars

    # Resumen por moneda (nota: en tu API "moneda" es id; si luego agregás moneda_codigo, esto mejora)
    per_moneda: Dict[str, Dict[str, Decimal]] = {}

    for m in day_moves:
        moneda_key = str(m["moneda"])  # MVP: id como string
        per_moneda.setdefault(moneda_key, {"compras_divisa": Decimal("0"), "ventas_divisa": Decimal("0")})

        if m["tipo"] == "compra":
            per_moneda[moneda_key]["compras_divisa"] += _to_decimal(m["monto_divisa"])
        else:
            per_moneda[moneda_key]["ventas_divisa"] += _to_decimal(m["monto_divisa"])

    # Calcular saldo del día por moneda (solo por movimientos de ese día)
    per_moneda_out = {}
    for k, v in per_moneda.items():
        saldo_dia = v["compras_divisa"] - v["ventas_divisa"]
        per_moneda_out[k] = {
            "compras_divisa": str(v["compras_divisa"]),
            "ventas_divisa": str(v["ventas_divisa"]),
            "saldo_dia_divisa": str(saldo_dia),
        }

    # Saldos actuales (globales)
    saldos_actuales = fetch_saldos_actuales()

    payload = {
        "meta": {
            "target_date": target_date,
            "api_base": API_BASE,
            "timezone_note": TIMEZONE_NOTE,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        },
        "kpis": {
            "total_compras_ars": str(compras_ars),
            "total_ventas_ars": str(ventas_ars),
            "resultado_neto_ars": str(resultado_ars),
            "cantidad_movimientos": len(day_moves),
        },
        "por_moneda_del_dia": per_moneda_out,
        "saldos_actuales": saldos_actuales,
        "movimientos_del_dia": day_moves,  # lo dejamos para GPT si querés análisis fino
    }
    return payload


if __name__ == "__main__":
    # Por defecto: ayer
    yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()

    target = os.getenv("TARGET_DATE", yesterday)
    data = build_daily_summary(target)
    print(json.dumps(data, ensure_ascii=False, indent=2))
