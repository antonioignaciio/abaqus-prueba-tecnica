from rest_framework import serializers

class EvolucionDiaSerializer(serializers.Serializer):
    fecha = serializers.DateField()
    valor_total = serializers.DecimalField(max_digits=20, decimal_places=2)
    weights = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=8))