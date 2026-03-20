from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MovimientoViewSet, SaldosAPIView, ResultadoAPIView, MonedaListAPIView, AIAnalysisAPIView

router = DefaultRouter()
router.register(r"movimientos", MovimientoViewSet, basename="movimiento")

urlpatterns = [
    # /api/movimientos/  (list, create)
    path("api/", include(router.urls)),

    # /api/saldos/
    path("api/saldos/", SaldosAPIView.as_view(), name="saldos"),

    # /api/resultado/
    path("api/resultado/", ResultadoAPIView.as_view(), name="resultado"),

    path("api/monedas/", MonedaListAPIView.as_view(), name="monedas"),
    path("api/ai/analysis/", AIAnalysisAPIView.as_view()),
]
