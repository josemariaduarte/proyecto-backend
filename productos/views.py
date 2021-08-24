from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from productos.models import SubCategoriaProducto, Categoria
from productos.permissions import PermisoSubCategoriaProducto, PermisoCategoriaProducto
from productos.serializers import SubCategoriaProductoSerializer, CategoriaProductoSerializer
from utils.paginations import GenericPagination
from utils.views import BaseModelViewSet


class SubCategoriaProductoViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar SubCategorias de Productos
    """

    retrieve_permissions = 'view_subcategoriaproducto'
    list_permissions = 'view_subcategoriaproducto'
    update_permissions = 'change_subcategoriaproducto'
    create_permissions = 'add_subcategoriaproducto'
    destroy_permissions = 'delete_subcategoriaproducto'
    activate_permissions = [PermisoSubCategoriaProducto.activar_subcategoriaproducto.perm]
    inactivate_permissions = [PermisoSubCategoriaProducto.inactivar_subcategoriaproducto.perm]
    # siempre se traen solo los activos
    queryset = SubCategoriaProducto.objects.filter(activo=True)
    #
    serializer_class = SubCategoriaProductoSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['nombre']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination


class CategoriaProductoViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar Categorias de Productos
    """

    retrieve_permissions = 'view_categoriaproducto'
    list_permissions = 'view_categoriaproducto'
    update_permissions = 'change_categoriaproducto'
    create_permissions = 'add_categoriaproducto'
    destroy_permissions = 'delete_categoriaproducto'
    activate_permissions = [PermisoCategoriaProducto.activar_categoriaproducto.perm]
    inactivate_permissions = [PermisoCategoriaProducto.inactivar_categoriaproducto.perm]
    #
    queryset = Categoria.objects.filter(activo=True)
    #
    serializer_class = CategoriaProductoSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['nombre']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination
