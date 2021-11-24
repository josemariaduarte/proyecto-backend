from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import model_meta

from movimientos.models import OrdenCompra, OrdenCompraDetalle, CompraDetalle, Compra, VentaDetalle, Venta, Caja, \
    MovimientoCaja
from productos.models import TransaccionProducto, Producto
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
        fields = ['id', 'producto', 'cantidad', 'precio', 'impuesto']


class CompraSerializer(BaseModelSerializer):
    """
    serializer de orden de compra
    """
    detalles = CompraDetalleSerializer(many=True, source='compradetalle_set', required=False)
    proveedor_name = serializers.CharField(source='proveedor.razon_social', required=False)
    condicion_choices = serializers.CharField(source='get_condicion_display', required=False)
    table_columns = ['fecha']

    class Meta:
        model = Compra
        fields = ['id',
                  'proveedor',
                  'proveedor_name',
                  'tipo_comprobante',
                  'numero_comprobante',
                  'condicion',
                  'total',
                  'fecha',
                  'detalles',
                  'total_iva5',
                  'total_iva10',
                  'total_excenta',
                  'activo',
                  'condicion_choices',
                  ]

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
        if producto.precio_compra != float(detail['precio']):
            producto.precio_compra = float(detail['precio'])
            producto.precio_venta = float(detail['precio']) + (float(detail['precio']) * (producto.porcentaje_ganancia/100))
            producto.fecha_modificacion_precio_venta = timezone.now()
            # creamos la transaccion producto
        producto.save()


    @transaction.atomic
    def create(self, validated_data):
        k = 'compradetalle_set'
        iva10 =0
        iva5=0
        ivaEx = 0
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
            # evaluamos el iva
            if detalle['impuesto'] == 10:
                iva10 += ((detalle['cantidad'] * detalle['precio'])*(10/100))
            elif detalle['impuesto'] == 5:
                iva5 += ((detalle['cantidad'] * detalle['precio'])*(5/100))
            else:
                ivaEx += (detalle['cantidad'] * detalle['precio'])
        #
        compra.total = monto
        compra.total_iva5 = iva5
        compra.total_iva10 = iva10
        compra.total_excenta = ivaEx
        compra.save()
        # CREAMOS EL MOVIMIENTO DE CAJA
        MovimientoCaja.objects.create(
            compra=compra,
            fecha=timezone.now(),
            tipo_movimiento=MovimientoCaja.COMPRA
        )
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
        iva10 = 0
        iva5 = 0
        ivaEx = 0
        for detalle in detalles:
            monto += (float(detalle['cantidad']) * float(detalle['precio']))
            if detalle['impuesto'] == 10:
                iva10 += ((float(detalle['cantidad']) * float(detalle['precio']))*(10/100))
            elif detalle['impuesto'] == 5:
                iva5 += ((float(detalle['cantidad']) * float(detalle['precio']))*(5/100))
            else:
                ivaEx += (float(detalle['cantidad']) * float(detalle['precio']))
        #
        compra.total = monto
        compra.total_iva5 = iva5
        compra.total_iva10 = iva10
        compra.total_excenta = ivaEx
        compra.save()
        return compra

    def update_detalles(self, compra, detalles):
        queryset = compra.compradetalle_set
        actuales = queryset.all()
        nuevos = [a for a in detalles if 'id' not in a.keys()]
        # Los elementos que esten en actuales y no esten en detalles son eliminados
        eliminados = list_diff([a['id'] for a in actuales.values('id')],
                               [a['id'] for a in detalles if 'id' in a.keys()])

        # for detalle in detalles:
        #     if 'id' in detalle.keys():
        #         changed_fields = []
        #         obj = CompraDetalle.objects.get(pk=detalle['id'])
        #         info = model_meta.get_field_info(obj)
        #         for attr, value in detalle.items():
        #             if attr in info.relations.keys():
        #                 attr += "_id"
        #             if getattr(obj, attr) != value:
        #                 changed_fields.append(attr)
        #             # actualizamos la cantidad del producto
        #             producto = obj.producto
        #             if attr == 'cantidad':
        #                 producto.cantidad = producto.cantidad + float(value) - obj.cantidad
        #                 producto.save()
        #             elif attr == 'precio':
        #                 # solo si se modifico el precio
        #                 if producto.precio_compra != float(value):
        #                     producto.precio_compra = float(value)
        #                     producto.precio_venta = float(value) + float(value) * (producto.porcentaje_ganancia / 100)
        #                     producto.fecha_modificacion_precio_venta = timezone.now()
        #                     producto.save()
        #             setattr(obj, attr, value)
        #         obj.save()
        #
        for data in nuevos:
            producto=Producto.objects.get(pk=data.get('producto'))
            CompraDetalle.objects.create(
                compra=compra,
                producto=producto,
                cantidad=data.get('cantidad'),
                precio=data.get('precio'),
                impuesto=data.get('impuesto')
            )
            #
            producto.cantidad += float(data.get('cantidad'))
            producto.fecha_ultima_compra = timezone.now()
            # si se cambio el precio de compra entonces se actualizan los precios
            if producto.precio_compra != float(data.get('precio')):
                producto.precio_compra = float(data.get('precio'))
                producto.precio_venta = float(data.get('precio')) + (
                            float(data.get('precio')) * (producto.porcentaje_ganancia / 100))
                producto.fecha_modificacion_precio_venta = timezone.now()
                # creamos la transaccion producto
            producto.save()
        #
        for obj in queryset.filter(pk__in=eliminados):
            # restamos la cantidad al stock al el
            producto = obj.producto
            producto.cantidad -= float(obj.cantidad)
            producto.save()
            obj.delete()


class VentaDetalleSerializer(BaseModelSerializer):
    """
    serializer de detalle de venta
    """
    producto_precio_venta = serializers.CharField(label="Precio", source='producto.precio_venta', required=False)
    producto_name = serializers.CharField(label="Nombre", source='producto.nombre', required=False)
    total = serializers.SerializerMethodField(method_name='get_total_calculado')
    table_columns = []

    class Meta:
        model = VentaDetalle
        fields = ['id', 'producto', 'producto_name', 'producto_precio_venta', 'cantidad', 'precio', 'impuesto', 'total']

    def get_total_calculado(self, instance):
        return instance.cantidad * instance.precio


class VentaSerializer(BaseModelSerializer):
    """
    serializer de ventas
    """
    detalles = VentaDetalleSerializer(many=True, source='ventadetalle_set', required=True)
    tipo_comprobante_name = serializers.CharField(label="Tipo Comprobante", source='get_tipo_comprobante_display', required=False)
    cliente_documento = serializers.CharField(label="Documento", source='cliente.nro_doc', required=False)
    cliente_direccion = serializers.CharField(label="Direccion", source='cliente.direccion', required=False)
    cliente_telefono = serializers.CharField(label="Telefono", source='cliente.telefono', required=False)
    cliente_name = serializers.ReadOnlyField()
    table_columns = ['fecha']

    class Meta:
        model = Venta
        fields = ['id',
                  'cliente',
                  'cliente_name',
                  'cliente_documento',
                  'cliente_direccion',
                  'cliente_telefono',
                  'tipo_comprobante',
                  'tipo_comprobante_name',
                  'numero_comprobante',
                  'condicion',
                  'total_iva5',
                  'total_iva10',
                  'total',
                  'fecha',
                  'detalles',
                  'activo']


    @transaction.atomic
    def create(self, validated_data):
        k = 'ventadetalle_set'
        iva10 = 0
        iva5 = 0
        ivaEx = 0
        monto = 0
        detalles = validated_data.pop(k, [])
        if k in validated_data:
            del validated_data[k]
        validated_data['usuario'] = self.context['request'].user
        venta = super(VentaSerializer, self).create(validated_data)
        for detalle in detalles:
            VentaDetalle.objects.create(venta=venta,
                                        producto=detalle.get('producto'),
                                        cantidad=detalle.get('cantidad'),
                                        precio=detalle.get('producto').precio_venta,
                                        precio_venta=detalle.get('precio'),
                                        impuesto=detalle.get('impuesto')
                                        ) # corresponde al precio que al final se vende
            monto += (detalle.get('cantidad') * detalle.get('precio'))
            # permite restar cantidades del producto
            producto = detalle.get('producto')
            producto.cantidad -= detalle.get('cantidad')
            producto.save()
            # evaluamos el iva
            if detalle['impuesto'] == 10:
                iva10 += (detalle.get('cantidad') * detalle.get('precio') * (10 / 100))
            elif detalle['impuesto'] == 5:
                iva5 += ((detalle.get('cantidad') * detalle.get('precio')) * (5 / 100))
            else:
                ivaEx += (detalle.get('cantidad') * detalle.get('precio'))
        #
        venta.total = monto
        venta.total_iva5 = iva5
        venta.total_iva10 = iva10
        venta.total_excenta = ivaEx
        venta.save()
        #
        MovimientoCaja.objects.create(
            venta=venta,
            fecha=timezone.now(),
            tipo_movimiento=MovimientoCaja.VENTA
        )
        #
        return venta



    @transaction.atomic
    def update(self, venta, validated_data):
        k = 'ventadetalle_set'
        if k in validated_data:
            del validated_data[k]
        venta = super(VentaSerializer, self).update(venta, validated_data)
        # actualizacion de dias
        detalles = self.initial_data.get('detalles', [])
        self.update_detalles(venta, detalles)
        # actualizamos los montos total
        monto = 0
        iva10 = 0
        iva5 = 0
        ivaEx = 0
        for detalle in detalles:
            monto += (float(detalle['cantidad']) * float(detalle['precio']))
            if detalle['impuesto'] == 10:
                iva10 += ((float(detalle['cantidad']) * float(detalle['precio'])) * (10 / 100))
            elif detalle['impuesto'] == 5:
                iva5 += ((float(detalle['cantidad']) * float(detalle['precio'])) * (5 / 100))
            else:
                ivaEx += (float(detalle['cantidad']) * float(detalle['precio']))
        #
        venta.total = monto
        venta.total_iva5 = iva5
        venta.total_iva10 = iva10
        venta.total_excenta = ivaEx
        venta.save()
        return venta


    def update_detalles(self, venta, detalles):
        queryset = venta.ventadetalle_set
        actuales = queryset.all()
        nuevos = [a for a in detalles if 'id' not in a.keys()]
        # Los elementos que esten en actuales y no esten en detalles son eliminados
        eliminados = list_diff([a['id'] for a in actuales.values('id')],
                               [a['id'] for a in detalles if 'id' in a.keys()])

        # for detalle in detalles:
        #     if 'id' in detalle.keys():
        #         changed_fields = []
        #         obj = CompraDetalle.objects.get(pk=detalle['id'])
        #         info = model_meta.get_field_info(obj)
        #         for attr, value in detalle.items():
        #             if attr in info.relations.keys():
        #                 attr += "_id"
        #             if getattr(obj, attr) != value:
        #                 changed_fields.append(attr)
        #             # actualizamos la cantidad del producto
        #             producto = obj.producto
        #             if attr == 'cantidad':
        #                 producto.cantidad = producto.cantidad + float(value) - obj.cantidad
        #                 producto.save()
        #             elif attr == 'precio':
        #                 # solo si se modifico el precio
        #                 if producto.precio_compra != float(value):
        #                     producto.precio_compra = float(value)
        #                     producto.precio_venta = float(value) + float(value) * (producto.porcentaje_ganancia / 100)
        #                     producto.fecha_modificacion_precio_venta = timezone.now()
        #                     producto.save()
        #             setattr(obj, attr, value)
        #         obj.save()

        for data in nuevos:
            producto=Producto.objects.get(pk=data.get('producto'))
            VentaDetalle.objects.create(
                venta=venta,
                producto=producto,
                cantidad=data.get('cantidad'),
                precio=producto.precio_venta,
                precio_venta=data.get('precio'),
                impuesto=data.get('impuesto')
            )

            producto.cantidad -= float(data.get('cantidad'))
            producto.save()
        #
        for obj in queryset.filter(pk__in=eliminados):
            # restamos la cantidad al stock al el
            producto = obj.producto
            producto.cantidad += float(obj.cantidad)
            producto.save()
            obj.delete()


class CajaSerializer(BaseModelSerializer):
    """
    serializer de caja
    """
    table_columns = ['id', 'fecha', 'monto', 'tipo_name']
    tipo_name = serializers.CharField(source='get_tipo_display', required=False, label='Tipo')
    fecha = serializers.DateField(required=False)

    class Meta:
        model = Caja
        fields = ['id', 'fecha', 'tipo', 'tipo_name', 'monto', 'activo']

    @transaction.atomic
    def create(self, validated_data):
        validated_data['fecha'] = timezone.now().date()
        caja = super(CajaSerializer, self).create(validated_data)
        ## CREAMOS UN MOVIMIENTO DE CAJA DE APERTURA
        MovimientoCaja.objects.create(
            caja=caja,
            fecha=timezone.now(),
            tipo_movimiento=MovimientoCaja.APERTURA
        )
        return caja


class MovimientoCajaSerializer(BaseModelSerializer):
    """
    serializer de movimiento de caja
    """

    table_columns = ['id', 'fecha', 'tipo_name']
    tipo_name = serializers.CharField(source='get_tipo_movimiento_display', required=False, label='Tipo Movimiento')
    monto = SerializerMethodField(label='Monto')
    comprobante = SerializerMethodField(label='Comprobante')

    class Meta:
        model = MovimientoCaja
        # fields = ['id', 'fecha', 'tipo_movimiento', 'tipo_name', 'monto', 'comprobante']
        fields = ('id', 'fecha', 'tipo_movimiento', 'tipo_name', 'monto', 'comprobante')

    def get_monto(self, instance):
        monto = 0
        if instance.venta and instance.venta.activo:
            monto = instance.venta.total
        elif instance.compra and instance.compra.activo:
            monto = instance.compra.total
        elif instance.caja:
            monto = instance.caja.monto
        return monto

    def get_comprobante(self, instance):
        comprobante = "Sin comprobante"
        if instance.venta and instance.venta.activo:
            comprobante = instance.venta.numero_comprobante
        elif instance.compra and instance.compra.activo:
            comprobante = instance.compra.numero_comprobante
        return comprobante
