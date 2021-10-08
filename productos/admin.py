from django.contrib import admin

# Register your models here.
from productos.models import Categoria, SubCategoriaProducto, Producto, TransaccionProducto

@admin.register(Categoria)
class CategoriaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre',  'activo']


@admin.register(SubCategoriaProducto)
class SubCategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'categoria_producto', 'activo']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio_venta', 'activo']


@admin.register(TransaccionProducto)
class TransaccionProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'cantidad']
