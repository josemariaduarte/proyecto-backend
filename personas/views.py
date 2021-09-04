from django.shortcuts import render
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from personas.permissions import PermisoProveedor
from personas.serializers import ProveedorSerializer, ClienteSerializer
from utils.paginations import GenericPagination
from utils.views import BaseModelViewSet
from personas.models import Proveedor, Cliente, Persona


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



class ClienteViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar SubCategorias de Productos
    """

    retrieve_permissions = 'view_cliente'
    list_permissions = 'view_cliente'
    update_permissions = 'change_cliente'
    create_permissions = 'add_cliente'
    destroy_permissions = 'delete_cliente'
    activate_permissions = [PermisoProveedor.activar_proveedor]
    inactivate_permissions = [PermisoProveedor.inactivar_proveedor.perm]
    #
    queryset = Cliente.objects.all()
    #
    serializer_class = ClienteSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['nombres']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination



@api_view(['GET'])
def get_sexo_choices(request):
    return Response(dict(sexo=[{'id': choice[0], 'text': choice[1]} for choice in Persona.SEXO_CHOICES]))


@api_view(['GET'])
def get_estado_civil(request):
    return Response(dict(estado_civil=[{'id': choice[0], 'text': choice[1]} for choice in Persona.ESTADO_CIVIL_CHOICES]))
