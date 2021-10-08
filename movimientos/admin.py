from django.contrib import admin

# Register your models here.
from movimientos.models import OrdenCompra, OrdenCompraDetalle, Compra, Venta, VentaDetalle


class OrdenCompraDetalleInline(admin.TabularInline):
    model = OrdenCompraDetalle
    extra = 0

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'fecha']
    inlines = [OrdenCompraDetalleInline]


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'fecha']


class VentaDetalleInline(admin.TabularInline):
    model = VentaDetalle
    extra = 0


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha']
    inlines = [VentaDetalleInline]
