from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from personas.models import Proveedor, Cliente
from productos.models import Producto


class Timbrado(models.Model):
    """
    modelo timbrado para las ventas
    """
    numero = models.CharField('Número', max_length=64)
    fecha_inicio = models.DateField('Fecha de inicio')
    fecha_fin = models.DateField('Fecha de finalización')
    codigo_establecimiento = models.CharField('Código de establecimiento', max_length=32)
    punto_expedicion = models.CharField('Punto de expedición', max_length=32)
    cantidad = models.IntegerField()
    rango_inicio = models.IntegerField()
    rango_fin = models.IntegerField()
    secuencia_actual = models.IntegerField()
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.numero


class OrdenCompra(models.Model):
    """
    modelo Orden de Compra
    """
    CREADO = 1
    APROBADO = 2
    RECHAZADO = 3
    ORDEN_COMPRA_ESTADO_CHOICES = (
        (CREADO, 'CREADO'),
        (APROBADO, 'APROBADO'),
        (RECHAZADO, 'RECHAZADO')
    )
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha')
    estado = models.IntegerField(choices=ORDEN_COMPRA_ESTADO_CHOICES, default=CREADO)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Orden Compra'
        verbose_name_plural = 'Ordenes de Compra'


class OrdenCompraDetalle(models.Model):
    """
    modelo Orden de Compra Detalle
    """
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.FloatField(verbose_name='Cantidad')
    precio = models.FloatField(verbose_name='Precio')
    fecha_creacion = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Orden Compra Detalle'
        verbose_name_plural = 'Ordenes de Compra Detalle'


class Compra(models.Model):
    """
    modelo Compra
    """
    TICKET = 1
    FACTURA = 2
    TIPO_COMPROBANTE_CHOICES = (
        (TICKET, 'TICKET'),
        (FACTURA, 'FACTURA')
    )
    CONTADO = 1
    CREDITO = 2
    CONDICION_COMPRA_CHOICES = (
        (CONTADO, 'CONTADO'),
        (CREDITO, 'CREDITO')
    )
    condicion = models.IntegerField(choices=CONDICION_COMPRA_CHOICES, default=CONTADO)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    tipo_comprobante = models.IntegerField(choices=TIPO_COMPROBANTE_CHOICES, default=FACTURA)
    numero_comprobante = models.CharField(max_length=100, verbose_name='Numero Comprobante', blank=True, null=True)
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha')
    total = models.FloatField(verbose_name='Total', default=0)
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.PROTECT, blank=True, null=True)
    total_iva5 = models.FloatField(verbose_name="Total IVA 5%", default=0)
    total_iva10 = models.FloatField(verbose_name="Total IVA 10%", default=0)
    total_excenta = models.FloatField(verbose_name="Total Excenta", default=0)
    #
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'


class CompraDetalle(models.Model):
    """
    modelo  Compra Detalle
    """
    IMPUESTO_CHOICES = (
        (5, '5%'),
        (10, '10%'),
        (0, 'EXCENTA')
    )
    impuesto = models.IntegerField(choices=IMPUESTO_CHOICES, default=10)
    compra = models.ForeignKey(Compra, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.FloatField(verbose_name='Cantidad')
    precio = models.FloatField(verbose_name='Precio')
    fecha_creacion = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Compra Detalle'
        verbose_name_plural = 'Compra Detalle'

    def __str__(self):
        return self.producto


class Venta(models.Model):
    """
    modelo Venta
    """
    TICKET = 1
    FACTURA = 2
    TIPO_COMPROBANTE_CHOICES = (
        (TICKET, 'TICKET'),
        (FACTURA, 'FACTURA')
    )
    IMPUESTO_CHOICES = (
        (5, '5%'),
        (10, '10%'),
        (0, 'EXCENTA')
    )
    CONTADO = 1
    CREDITO = 2
    CONDICION_VENTA_CHOICES = (
        (CONTADO, 'CONTADO'),
        (CREDITO, 'CREDITO')
    )
    condicion = models.IntegerField(choices=CONDICION_VENTA_CHOICES, default=CONTADO)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    tipo_comprobante = models.IntegerField(choices=TIPO_COMPROBANTE_CHOICES, default=FACTURA)
    timbrado = models.ForeignKey(Timbrado, on_delete=models.PROTECT, blank=True, null=True)
    numero_comprobante = models.CharField(max_length=100, verbose_name='Numero Comprobante', blank=True, null=True)
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha')
    impuesto = models.IntegerField(choices=IMPUESTO_CHOICES, blank=True, null=True)
    total = models.FloatField(verbose_name='Total', default=0)
    total_iva5 = models.FloatField(verbose_name="Total IVA 5%", default=0)
    total_iva10 = models.FloatField(verbose_name="Total IVA 10%", default=0)
    total_excenta = models.FloatField(verbose_name="Total Excenta", default=0)

    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    @property
    def cliente_name(self):
        return self.cliente.get_full_name


class VentaDetalle(models.Model):
    """
    modelo  Venta Detalle
    """
    IMPUESTO_CHOICES = (
        (5, '5%'),
        (10, '10%'),
        (0, 'EXCENTA')
    )
    impuesto = models.IntegerField(choices=IMPUESTO_CHOICES, default=10)
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.FloatField(verbose_name='Cantidad')
    precio = models.FloatField(verbose_name='Precio')
    precio_venta = models.FloatField(verbose_name='Precio Venta')

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Venta Detalle'
        verbose_name_plural = 'Ventas Detalle'

    def __str__(self):
        return self.producto


class Caja(models.Model):
    """
    modelo de Caja
    """
    APERTURA = 1
    CIERRE = 2
    TIPO_CAJA = (
        (APERTURA, 'APERTURA'),
        (CIERRE, 'CIERRE')
    )
    fecha = models.DateField(verbose_name='Fecha')
    monto = models.FloatField(verbose_name='Total', default=0)
    tipo = models.IntegerField(choices=TIPO_CAJA, default=APERTURA)
    facturas = models.CharField(verbose_name='Facturas', blank=True, null=True, max_length=255)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'


class MovimientoCaja(models.Model):
    """
       modelo de Movimiento de Caja(es para hacer el calculo de entrada/salida)
    """
    COMPRA = 1
    VENTA = 2
    APERTURA = 3
    TIPO_MOVIMIENTO_CHOICES = (
        (COMPRA, 'COMPRA'),
        (VENTA, 'VENTA'),
        (APERTURA, 'APERTURA')
    )
    tipo_movimiento = models.IntegerField(verbose_name='Tipo', choices=TIPO_MOVIMIENTO_CHOICES, default=VENTA)
    compra = models.ForeignKey(Compra, on_delete=models.PROTECT, blank=True, null=True)
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, blank=True, null=True)
    fecha = models.DateField(verbose_name='Fecha')
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT, blank=True, null=True)
    cerrado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Movimiento de Caja'
        verbose_name_plural = 'Movimientos de Caja'