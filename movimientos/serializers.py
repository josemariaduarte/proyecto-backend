from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.utils import model_meta

from movimientos.models import OrdenCompra, OrdenCompraDetalle, CompraDetalle, Compra
from productos.models import TransaccionProducto
from utils.functions import list_diff
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
    proveedor_name = serializers.CharField(source='proveedor.razon_social', required=False)
    table_columns = ['fecha']

    class Meta:
        model = Compra
        fields = ['id', 'proveedor', 'proveedor_name', 'tipo_comprobante', 'numero_comprobante', 'impuesto', 'total', 'fecha', 'detalles']

    def producto_actualizar(self, detail):
        '''
        permite actualizar datos del producto
        :param detail: detalle de compra
        :return: true
        '''
        producto = detail['producto']
        cantidad_anterior = producto.cantidad
        precio_compra_anterior = producto.precio_compra
        precio_venta_anterior = producto.precio_venta
        producto.cantidad = producto.cantidad + detail['cantidad']
        producto.fecha_ultima_compra = timezone.now()
        # si se cambio el precio de compra entonces se actualizan los precios
        if producto.precio_compra != float(detail['precio']):
            producto.precio_compra = float(detail['precio'])
            producto.precio_venta += float(detail['precio']) * (producto.porcentaje_ganancia/100)
            producto.fecha_modificacion_precio_venta = timezone.now()
            # creamos la transaccion producto
        producto.save()
        #
        TransaccionProducto.objects.create(
            producto=detail['producto'],
            cantidad=float(detail['cantidad']),
            cantidad_anterior=cantidad_anterior,
            cantidad_actual=producto.cantidad,
            precio_compra_anterior=precio_compra_anterior,
            precio_compra=producto.precio_compra,
            precio_venta_anterior=precio_venta_anterior,
            precio_venta=producto.precio_venta
        )



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

    @transaction.atomic
    def update(self, compra, validated_data):
        k = 'compradetalle_set'
        if k in validated_data:
            del validated_data[k]
        compra = super(CompraSerializer, self).update(compra, validated_data)
        # actualizacion de dias
        detalles = self.initial_data.get('detalles', [])
        self.update_detalles(compra, detalles)
        # actualizamos los montos total
        monto = 0
        for detalle in detalles:
            monto += (float(detalle['cantidad']) * float(detalle['precio']))
        #
        compra.total = monto
        compra.save()
        return compra

    def update_detalles(self, compra, detalles):
        queryset = compra.compradetalle_set
        actuales = queryset.all()
        nuevos = [a for a in detalles if 'id' not in a.keys()]
        # Los elementos que esten en actuales y no esten en detalles son eliminados
        eliminados = list_diff([a['id'] for a in actuales.values('id')],
                               [a['id'] for a in detalles if 'id' in a.keys()])

        for detalle in detalles:
            if 'id' in detalle.keys():
                changed_fields = []
                obj = CompraDetalle.objects.get(pk=detalle['id'])
                info = model_meta.get_field_info(obj)
                for attr, value in detalle.items():
                    if attr in info.relations.keys():
                        attr += "_id"
                    if getattr(obj, attr) != value:
                        changed_fields.append(attr)
                    # actualizamos la cantidad del producto
                    producto = obj.producto
                    if attr == 'cantidad':
                        producto.cantidad = producto.cantidad + float(value) - obj.cantidad
                        producto.save()
                    elif attr == 'precio':
                        # solo si se modifico el precio
                        if producto.precio_compra != float(value):
                            producto.precio_compra = float(value)
                            producto.precio_venta += float(value) * (producto.porcentaje_ganancia / 100)
                            producto.fecha_modificacion_precio_venta = timezone.now()
                            producto.save()
                    setattr(obj, attr, value)
                obj.save()
        #
        for data in nuevos:
            CompraDetalle.objects.create(compra=compra, **data)
        #
        for obj in queryset.filter(pk__in=eliminados):
            obj.delete()












