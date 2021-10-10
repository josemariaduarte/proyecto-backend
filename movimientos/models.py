from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from personas.models import Proveedor, Cliente
from productos.models import Producto


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
    IMPUESTO_CHOICES = (
        (5, '5%'),
        (10, '10%')
    )

    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    tipo_comprobante = models.IntegerField(choices=TIPO_COMPROBANTE_CHOICES, default=FACTURA)
    numero_comprobante = models.CharField(max_length=100, verbose_name='Numero Comprobante', blank=True, null=True)
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha')
    impuesto = models.IntegerField(choices=IMPUESTO_CHOICES, blank=True, null=True)
    total = models.FloatField(verbose_name='Total', default=0)
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.PROTECT, blank=True, null=True)

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
        (10, '10%')
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    tipo_comprobante = models.IntegerField(choices=TIPO_COMPROBANTE_CHOICES, default=FACTURA)
    numero_comprobante = models.CharField(max_length=100, verbose_name='Numero Comprobante', blank=True, null=True)
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha')
    impuesto = models.IntegerField(choices=IMPUESTO_CHOICES, blank=True, null=True)
    total = models.FloatField(verbose_name='Total', default=0)

    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    @property
    def cliente_name(self):
        return self.cliente.get_full_name



class VentaDetalle(models.Model):
    """
    modelo  Venta Detalle
    """
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
