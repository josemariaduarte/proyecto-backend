from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.filters import SearchFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from movimientos.models import OrdenCompra, Compra, OrdenCompraDetalle, CompraDetalle
from movimientos.permissions import PermisoOrdenCompra
from movimientos.serializers import OrdenCompraSerializer
from utils.messages import Success
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
