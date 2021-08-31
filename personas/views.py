from django.shortcuts import render
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from personas.permissions import PermisoProveedor
from personas.serializers import ProveedorSerializer
from utils.paginations import GenericPagination
from utils.views import BaseModelViewSet
from personas.models import Proveedor


class ProveedorViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar SubCategorias de Productos
    """

    retrieve_permissions = 'view_proveedor'
    list_permissions = 'view_proveedor'
    update_permissions = 'change_proveedor'
    create_permissions = 'add_proveedor'
    destroy_permissions = 'delete_proveedor'
    activate_permissions = [PermisoProveedor.activar_proveedor]
    inactivate_permissions = [PermisoProveedor.inactivar_proveedor.perm]
    #
    queryset = Proveedor.objects.all()
    #
    serializer_class = ProveedorSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['nombre']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination
