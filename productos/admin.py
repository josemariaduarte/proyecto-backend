from django.contrib import admin

# Register your models here.
from productos.models import Categoria, SubCategoriaProducto

@admin.register(Categoria)
class CategoriaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre',  'activo']


@admin.register(SubCategoriaProducto)
class SubCategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'categoria_producto', 'activo']