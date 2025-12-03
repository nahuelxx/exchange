from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MovimientoViewSet, SaldosAPIView, ResultadoAPIView

router = DefaultRouter()
router.register(r"movimientos", MovimientoViewSet, basename="movimiento")

urlpatterns = [
    # /api/movimientos/  (list, create)
    path("api/", include(router.urls)),

    # /api/saldos/
    path("api/saldos/", SaldosAPIView.as_view(), name="saldos"),

    # /api/resultado/
    path("api/resultado/", ResultadoAPIView.as_view(), name="resultado"),
]
