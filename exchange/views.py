from rest_framework import mixins, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ai.analyzer import analyze_exchange_data
from .services.stats import build_daily_stats

from .models import Movimiento, Moneda
from .serializers import MovimientoSerializer, MonedaSerializer
from .mixins import BalanceMixin
from .utils import calcular_resultado_periodo

class MovimientoViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    ViewSet para listar y crear movimientos.

    - GET /api/movimientos/
    - POST /api/movimientos/
    """

    queryset = Movimiento.objects.all().order_by("-fecha", "-creado")
    serializer_class = MovimientoSerializer

class SaldosAPIView(BalanceMixin, APIView):
    """
    Devuelve los saldos actuales por moneda.

    GET /api/saldos/

    Response:
    {
      "USD": "120.00",
      "EUR": "40.00",
      ...
    }
    """

    def get(self, request, *args, **kwargs):
        saldos = {}
        queryset = Movimiento.objects.all()

        for moneda in Moneda.objects.all():
            saldo = self.calcular_saldo_moneda(moneda, queryset=queryset)
            saldos[moneda.codigo_iso] = str(saldo)

        return Response(saldos, status=status.HTTP_200_OK)

from datetime import datetime, time
from django.utils.timezone import make_aware, is_naive


class ResultadoAPIView(APIView):
    """
    Calcula el resultado (ganancia/pérdida) en ARS
    para un rango de fechas.

    GET /api/resultado/?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD

    Response:
    {
      "fecha_inicio": "2025-01-01",
      "fecha_fin": "2025-01-31",
      "resultado_ars": "11500.00"
    }
    """

    def _parse_fecha(self, valor: str):
        try:
            # Asumimos formato YYYY-MM-DD
            d = datetime.strptime(valor, "%Y-%m-%d").date()
            return d
        except (TypeError, ValueError):
            return None

    def get(self, request, *args, **kwargs):
        fecha_inicio_str = request.query_params.get("fecha_inicio")
        fecha_fin_str = request.query_params.get("fecha_fin")

        if not fecha_inicio_str or not fecha_fin_str:
            return Response(
                {
                    "detail": "Debe proporcionar fecha_inicio y fecha_fin en formato YYYY-MM-DD."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        fecha_inicio_date = self._parse_fecha(fecha_inicio_str)
        fecha_fin_date = self._parse_fecha(fecha_fin_str)

        if not fecha_inicio_date or not fecha_fin_date:
            return Response(
                {"detail": "Formato de fecha inválido. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convertimos a datetimes que abarcan todo el día
        inicio_dt = datetime.combine(fecha_inicio_date, time.min)
        fin_dt = datetime.combine(fecha_fin_date, time.max)

        if is_naive(inicio_dt):
            inicio_dt = make_aware(inicio_dt)
        if is_naive(fin_dt):
            fin_dt = make_aware(fin_dt)

        resultado = calcular_resultado_periodo(inicio_dt, fin_dt)

        data = {
            "fecha_inicio": fecha_inicio_date.isoformat(),
            "fecha_fin": fecha_fin_date.isoformat(),
            "resultado_ars": str(resultado),
        }
        return Response(data, status=status.HTTP_200_OK)
    
class MonedaListAPIView(generics.ListAPIView):
    queryset = Moneda.objects.all().order_by("codigo_iso")
    serializer_class = MonedaSerializer

class AIAnalysisAPIView(APIView):

    def get(self, request):

        fecha = request.query_params.get("fecha")
        question = request.query_params.get("q")

        stats = build_daily_stats(fecha)

        answer = analyze_exchange_data(stats, question)

        return Response({
            "analysis": answer
        })