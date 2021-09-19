from django.db import transaction
from rest_framework import serializers

from movimientos.models import OrdenCompra, OrdenCompraDetalle
from utils.serializers import BaseModelSerializer

class OrdenCompraDetalleSerializer(BaseModelSerializer):
    """
    serializer de detalle de orden de compra
    """
    table_columns = []

    class Meta:
        model = OrdenCompraDetalle
        fields = ['id', 'producto', 'cantidad', 'precio']


class OrdenCompraSerializer(BaseModelSerializer):
    """
    serializer de orden de compra
    """
    detalles = OrdenCompraDetalleSerializer(many=True, source='ordencompradetalle_set', required=False)
    estado = serializers.CharField(source='get_estado_display', required=False)
    proveedor_name = serializers.CharField(source='proveedor.razon_social', required=False)
    table_columns = ['fecha']

    class Meta:
        model = OrdenCompra
        fields = ['id', 'proveedor', 'proveedor_name', 'fecha', 'estado', 'detalles']

    @transaction.atomic
    def create(self, validated_data):
        k = 'ordencompradetalle_set'
        detalles = validated_data.pop(k, [])
        if k in validated_data:
            del validated_data[k]
        validated_data['usuario'] = self.context['request'].user
        orden = super(OrdenCompraSerializer, self).create(validated_data)

        for detalle in detalles:
            OrdenCompraDetalle.objects.create(orden_compra=orden, **detalle)
        #
        return orden



