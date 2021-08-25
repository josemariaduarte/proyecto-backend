from django.contrib import admin

# Register your models here.
from productos.models import Categoria

@admin.register(Categoria)
class CategoriaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre',  'activo']
