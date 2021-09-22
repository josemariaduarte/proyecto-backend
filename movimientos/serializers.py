from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from movimientos.models import OrdenCompra, OrdenCompraDetalle, CompraDetalle, Compra
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




class CompraDetalleSerializer(BaseModelSerializer):
    """
    serializer de detalle de compra
    """
    table_columns = []

    class Meta:
        model = CompraDetalle
        fields = ['id', 'producto', 'cantidad', 'precio']


class CompraSerializer(BaseModelSerializer):
    """
    serializer de orden de compra
    """
    detalles = CompraDetalleSerializer(many=True, source='compradetalle_set', required=False)

    table_columns = ['fecha']

    class Meta:
        model = Compra
        fields = ['id', 'proveedor', 'tipo_comprobante', 'numero_comprobante', 'impuesto', 'total', 'fecha', 'detalles']

    def producto_actualizar(self, detail):
        '''
        permite actualizar datos del producto
        :param detail: detalle de compra
        :return: true
        '''
        producto = detail['producto']
        producto.cantidad = producto.cantidad + detail['cantidad']
        producto.fecha_ultima_compra = timezone.now()
        # si se cambio el precio de compra entonces se actualizan los precios
        if producto.precio_compra != detail['precio']:
            producto.precio_compra = detail['precio']
            producto.precio_venta += detail['precio'] * (producto.porcentaje_ganancia/100)
            producto.fecha_modificacion_precio_venta = timezone.now()
        producto.save()



    @transaction.atomic
    def create(self, validated_data):
        k = 'compradetalle_set'
        detalles = validated_data.pop(k, [])
        if k in validated_data:
            del validated_data[k]
        validated_data['usuario'] = self.context['request'].user
        compra = super(CompraSerializer, self).create(validated_data)
        monto = 0
        for detalle in detalles:
            CompraDetalle.objects.create(compra=compra, **detalle)
            monto += (detalle['cantidad'] * detalle['precio'])
            self.producto_actualizar(detalle)
        #
        compra.total = monto
        compra.save()
        #
        return compra













