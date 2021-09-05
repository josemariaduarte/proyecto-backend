from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from productos.models import SubCategoriaProducto, Categoria, UnidadDeMedida, Deposito, Producto
from productos.permissions import PermisoSubCategoriaProducto, PermisoCategoriaProducto, PermisoUnidadDeMedida, \
    PermisoDeposito, PermisoProducto
from productos.serializers import SubCategoriaProductoSerializer, CategoriaProductoSerializer, UnidadDeMedidaSerializer, \
    DepositoSerializer, ProductoSerializer
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
    queryset = SubCategoriaProducto.objects.all()
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
    queryset = Categoria.objects.all()
    #
    serializer_class = CategoriaProductoSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['nombre']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination


class UnidadMedidaViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar Categorias de Productos
    """

    retrieve_permissions = 'view_unidadmedida'
    list_permissions = 'view_unidadmedida'
    update_permissions = 'change_unidadmedida'
    create_permissions = 'add_unidadmedida'
    destroy_permissions = 'delete_unidadmedida'
    activate_permissions = [PermisoUnidadDeMedida.activar_unidaddemedida.perm]
    inactivate_permissions = [PermisoUnidadDeMedida.inactivar_unidaddemedida.perm]
    #
    queryset = UnidadDeMedida.objects.all()
    #
    serializer_class = UnidadDeMedidaSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['nombre']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination


class DepositoViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar Depositos
    """

    retrieve_permissions = 'view_deposito'
    list_permissions = 'view_deposito'
    update_permissions = 'change_deposito'
    create_permissions = 'add_deposito'
    destroy_permissions = 'delete_deposito'
    activate_permissions = [PermisoDeposito.activar_deposito.perm]
    inactivate_permissions = [PermisoDeposito.inactivar_deposito.perm]
    #
    queryset = Deposito.objects.all()
    #
    serializer_class = DepositoSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['nombre']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination


class ProductoViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar Depositos
    """

    retrieve_permissions = 'view_producto'
    list_permissions = 'view_producto'
    update_permissions = 'change_producto'
    create_permissions = 'add_producto'
    destroy_permissions = 'delete_producto'
    activate_permissions = [PermisoProducto.activar_producto.perm]
    inactivate_permissions = [PermisoProducto.inactivar_producto.perm]
    #
    queryset = Producto.objects.all()
    #
    serializer_class = ProductoSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['nombre']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination