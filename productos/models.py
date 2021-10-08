from django.db import models

# Create your models here.
from personas.models import Proveedor
from productos.permissions import PermisoCategoriaProducto, PermisoSubCategoriaProducto, PermisoUnidadDeMedida, \
    PermisoDeposito, PermisoProveedor, PermisoProducto


class Categoria(models.Model):
    """
    modelo Categoria para Productos
    """

    nombre = models.CharField(verbose_name='Nombre', max_length=30)
    descripcion = models.CharField(verbose_name='Descripción', max_length=150, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Categoria de Producto'
        verbose_name_plural = 'Categorias de Productos'
        permissions = PermisoCategoriaProducto.get_permissions()

    def __str__(self):
        return self.nombre

    # overwrite save method
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        return super(Categoria, self).save(*args, **kwargs)


class SubCategoriaProducto(models.Model):
    """
    modelo SubCategoria para Productos
    """

    nombre = models.CharField(verbose_name='Nombre', max_length=100)
    descripcion = models.CharField(verbose_name='Descripción', max_length=150, blank=True, null=True)
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Sub-Categoria de Producto'
        verbose_name_plural = 'Sub-Categorias de Producto'
        permissions = PermisoSubCategoriaProducto.get_permissions()


class UnidadDeMedida(models.Model):
    """
    modelo Unidad de medida, relacionado a productos
    """

    nombre = models.CharField(verbose_name='Nombre', max_length=100)
    descripcion = models.CharField(verbose_name='Descripción', max_length=150, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Unidad de medida de Producto'
        verbose_name_plural = 'Unidades de medidas de Productos'
        permissions = PermisoUnidadDeMedida.get_permissions()

    def __str__(self):
        return self.nombre

    # overwrite save method
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        return super(UnidadDeMedida, self).save(*args, **kwargs)


class Deposito(models.Model):
    """
    modelo Deposito, relacionado a productos
    """

    nombre = models.CharField(verbose_name='Nombre', max_length=100)
    descripcion = models.CharField(verbose_name='Descripción', max_length=150, blank=True, null=True)
    direccion = models.CharField(verbose_name='Dirección', max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Deposito de Producto'
        verbose_name_plural = 'Depositos de Productos'
        permissions = PermisoDeposito.get_permissions()

    def __str__(self):
        return '{} -direcion: {}'.format(self.nombre, self.direccion)

    # overwrite save method
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        if self.direccion:
            self.direccion = self.direccion.upper()
        return super(Deposito, self).save(*args, **kwargs)




class Producto(models.Model):
    """
    modelo Producto
    """
    nombre = models.CharField(verbose_name='Nombre', max_length=100)
    descripcion = models.CharField(verbose_name='Descripción', max_length=100, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    fecha_ultima_compra = models.DateTimeField(verbose_name='Fecha Última Compra', blank=True, null=True)
    fecha_modificacion_precio_venta = models.DateTimeField(verbose_name='Fecha Modificación Precio Venta',
                                                           blank=True, null=True)
    precio_compra = models.FloatField(verbose_name='Precio Compra')
    precio_venta = models.FloatField(verbose_name='Precio Venta')
    cantidad = models.FloatField(verbose_name='Cantidad')
    cantidad_minima_stock = models.FloatField(verbose_name='Cantidad Minima Stock')
    subcategoria = models.ForeignKey(SubCategoriaProducto, on_delete=models.PROTECT)
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT)
    unidad_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.PROTECT)
    porcentaje_ganancia = models.FloatField(verbose_name='Porcentaje Ganancia', default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        permissions = PermisoProducto.get_permissions()

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.cantidad)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        return super(Producto, self).save(*args, **kwargs)


class TransaccionProducto(models.Model):
    """
    modelo para guardar los movimientos de un producto en compra/venta y el manejo de las cantidades y precios
    como un historico
    """
    COMPRA = 1
    VENTA = 2
    TIPO_TRANSACCION_PRODUCTO = (
        ('COMPRA', COMPRA),
        ('VENTA', VENTA),
    )
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    tipo = models.IntegerField(verbose_name='Tipo', choices=TIPO_TRANSACCION_PRODUCTO, default=COMPRA)
    cantidad = models.FloatField('Cantidad')
    cantidad_anterior = models.FloatField('Cantidad Anterior en Stock')
    cantidad_actual = models.FloatField('Cantidad Actual en Stock')
    precio_compra = models.FloatField(verbose_name='Precio Compra')
    precio_compra_anterior = models.FloatField(verbose_name='Precio Compra Anterior')
    precio_venta = models.FloatField(verbose_name='Precio Venta')
    precio_venta_anterior = models.FloatField(verbose_name='Precio Venta Anterior', default=0)


    class Meta:
        ordering = ['-pk']
        verbose_name = 'Transacción Producto'
        verbose_name_plural = 'Transacciones de Producto'
