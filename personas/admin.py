from django.contrib import admin

# Register your models here.
from personas.models import Cliente, Proveedor


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'activo']


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['razon_social', 'ruc', 'activo']
