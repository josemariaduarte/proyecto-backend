from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, api_view
from rest_framework.filters import SearchFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from movimientos.models import OrdenCompra, Compra, OrdenCompraDetalle, CompraDetalle
from movimientos.permissions import PermisoOrdenCompra
from movimientos.serializers import OrdenCompraSerializer, CompraSerializer
from utils.messages import Success, Error, Info
from utils.paginations import GenericPagination
from utils.views import BaseModelViewSet


class OrdenCompraViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar Ordenes de Compra
    """

    retrieve_permissions = 'view_orden_compra'
    list_permissions = 'view_orden_compra'
    update_permissions = 'change_orden_compra'
    create_permissions = 'add_orden_compra'
    destroy_permissions = 'delete_orden_Compra'
    activate_permissions = [PermisoOrdenCompra.activar_orden_compra.perm]
    inactivate_permissions = [PermisoOrdenCompra.inactivar_orden_compra.perm]
    #
    queryset = OrdenCompra.objects.all()
    #
    serializer_class = OrdenCompraSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['producto']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination

    @detail_route(methods=['post'])
    @transaction.atomic
    def aprobar(self, request, pk=None):
        instance = self.get_object()
        instance.estado = OrdenCompra.APROBADO
        instance.save()
        # creamos la compra
        compra = Compra.objects.create(orden_compra=instance,
                                       proveedor=instance.proveedor,
                                       fecha=instance.fecha,
                                       usuario=request.user)
        # creamos los detalles, para eso recorremos los detalles del orden de compra
        for detalle in OrdenCompraDetalle.objects.filter(orden_compra=instance):
            CompraDetalle.objects.create(compra=compra,
                                         producto=detalle.producto,
                                         cantidad=detalle.cantidad,
                                         precio=detalle.precio
                                         )
        return Response(dict(message=Success.ORDEN_APROBADO), status=status.HTTP_200_OK)


    @detail_route(methods=['post'])
    @transaction.atomic
    def rechazar(self, request, pk=None):
        instance = self.get_object()
        instance.estado = OrdenCompra.RECHAZADO
        instance.save()
        return Response(dict(message=Success.ORDEN_APROBADO), status=status.HTTP_200_OK)


class CompraViewSet(BaseModelViewSet):
    """
    API que permite crear, ver o editar Ordenes de Compra
    """

    retrieve_permissions = 'view_compra'
    list_permissions = 'view_compra'
    update_permissions = 'change_compra'
    create_permissions = 'add_compra'
    destroy_permissions = 'delete_compra'
    # quitamos activar e inactivar por que no lo vamos a usar de manera momentanea
    # activate_permissions = [PermisoOrdenCompra.activar_orden_compra.perm]
    # inactivate_permissions = [PermisoOrdenCompra.inactivar_orden_compra.perm]
    #
    queryset = Compra.objects.all()
    #
    serializer_class = CompraSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['proveedor']
    ordering_fields = ['id']
    ordering = ['-id']
    pagination_class = GenericPagination

    @detail_route(methods=['post'])
    def inactivar(self, request, pk=None):
        if not request.user.has_perms(self.inactivate_permissions):
            raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
        obj = self.get_object()
        if not hasattr(obj, 'activo'):
            raise ValidationError(dict(detail=Error.NO_TIENE_CAMPO_ACTIVO))
        if obj.activo == "N" or (obj.activo is not True and obj.activo != "S"):
            raise ValidationError(dict(detail=Info.INACTIVO))

        obj.activo = False
        obj.save()
        # descontamos del stock del producto

        return Response(dict(message=Success.INACTIVADO), status=status.HTTP_200_OK)



@api_view(['GET'])
def get_tipo_comprobante_choices(request):
    return Response(dict(tipo_comprobante=[{'id': choice[0], 'text': choice[1]} for choice in Compra.TIPO_COMPROBANTE_CHOICES]))


@api_view(['GET'])
def get_impuesto_choices(request):
    return Response(dict(impuesto=[{'id': choice[0], 'text': choice[1]} for choice in Compra.IMPUESTO_CHOICES]))









