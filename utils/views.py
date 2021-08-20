from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import list_route,  detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from proyecto.settings import REST_FRAMEWORK
from utils.messages import Error, Success, Info


class BaseModelViewSet(viewsets.ModelViewSet):
    retrieve_permissions = []
    update_permissions = []
    create_permissions = []
    list_permissions = []
    destroy_permissions = []
    revert_permissions = []
    activate_permissions = []
    inactivate_permissions = []
    permission_classes = [IsAuthenticated]

    filterset_fields = []
    page_size = REST_FRAMEWORK.get('PAGE_SIZE', 10)

    def initial(self, request, *args, **kwargs):
        self.page_size = request.GET.get('page_size', REST_FRAMEWORK.get('PAGE_SIZE', 10))
        if self.page_size and self.pagination_class:
            self.pagination_class.page_size = self.page_size
        if hasattr(self.serializer_class, 'filterset_fields'):
            self.filterset_fields = self.serializer_class.filterset_fields
        if hasattr(self, 'filterset_class'):
            self.filterset_fields = self.filterset_class.Meta.fields
        super(BaseModelViewSet, self).initial(request, *args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        filter[self.lookup_field] = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        if not request.user.has_perms(self.list_permissions):
            raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
        #
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = {"results": serializer.data,
                    "tableColumns": serializer.child.get_table_columns(),
                    "pageSize": self.page_size
                    }
            return self.get_paginated_response(data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET'], )
    def view(self, request, pk=None):
        if not request.user.has_perms(self.retrieve_permissions):
            raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
        serializer = self.get_serializer(self.get_object())
        return Response((serializer.data), status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if not request.user.has_perms(self.update_permissions):
            raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
        return super(BaseModelViewSet, self).update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perms(self.create_permissions):
            raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
        return super(BaseModelViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        raise NotImplementedError('No ser permite eliminar este registro')

    @detail_route(methods=['post'])
    def activar(self, request, pk=None):
        if not request.user.has_perms(self.activate_permissions):
            raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
        instance = self.get_object()
        if not hasattr(instance, 'activo'):
            raise ValidationError(dict(detail=Error.NO_TIENE_CAMPO_ACTIVO))
        if instance.activo:
            raise ValidationError(dict(detail=Info.ACTIVO))
        #
        assert getattr(self, 'activate_permissions', None), (
            Error.CAMPO_NULO.format(
                serializer_class=self.__class__.__name__,
                campo='activate_permissions'
            )
        )
        instance.activo = True
        instance.save()
        return Response(dict(message=Success.ACTIVADO), status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def inactivar(self, request, pk=None):
        if not request.user.has_perms(self.inactivate_permissions):
            raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
        obj = self.get_object()
        if not hasattr(obj, 'activo'):
            raise ValidationError(dict(detail=Error.NO_TIENE_CAMPO_ACTIVO))
        if obj.activo == "N" or (obj.activo is not True and obj.activo != "S"):
            raise ValidationError(dict(detail=Info.INACTIVO))

        # Nos cercioramos de que fue seteada la actividad
        assert getattr(self, 'inactivate_permissions', None), (
            Error.CAMPO_NULO.format(
                serializer_class=self.__class__.__name__,
                campo='inactivate_permissions'
            )
        )
        obj.activo = False
        obj.save()
        return Response(dict(message=Success.INACTIVADO), status=status.HTTP_200_OK)

