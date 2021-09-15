from django.contrib import admin

# Register your models here.
from movimientos.models import OrdenCompra, OrdenCompraDetalle, Compra


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
