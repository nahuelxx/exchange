from rest_framework import serializers
from .models import Movimiento


class MovimientoSerializer(serializers.ModelSerializer):
    """
    Serializer básico para el modelo Movimiento.

    - Usa el ModelSerializer para mapear todos los campos del MVP.
    - Delegamos las invariantes (positividad, total_ars) al modelo
      vía full_clean(), que es ejecutado en create/update.
    """

    class Meta:
        model = Movimiento
        fields = [
            "id",
            "fecha",
            "tipo",
            "moneda",
            "monto_divisa",
            "cotizacion",
            "total_ars",
            "fuente",
            "notas",
            "creado",
            "actualizado",
        ]
        read_only_fields = [
            "total_ars",   # lo calcula el modelo
            "creado",
            "actualizado",
        ]

    def create(self, validated_data):
        # El modelo se encarga de total_ars e invariantes en full_clean()
        instance = Movimiento(**validated_data)
        instance.full_clean()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save()
        return instance
