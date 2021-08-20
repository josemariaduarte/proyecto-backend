from django.contrib.auth import get_user_model
from django.contrib.auth.backends import UserModel
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.state import token_backend

from usuarios.serializers import UserSerializer, PasswordSerializer, MyRefreshToken, MyTokenObtainPairSerializer
from rest_framework import filters, status


@api_view(http_method_names=['POST'])
@permission_classes([])
def my_token_pair_view(request):
    serializer = MyTokenObtainPairSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@permission_classes([])
def token_permissions(request):
    """
        funcion que permite obtener los permisos de un usuario
    :param request:
    :return:
    """
    data = {}
    data['rules'] = MyRefreshToken.get_user_permissions(request.user)
    data["is_superuser"] = request.user.is_superuser
    token = token_backend.encode(data)
    return Response({'result': token}, status=status.HTTP_200_OK)


# class UserViewSet(BaseModelViewSet):
#     """
#         API que permite crear, ver o editar usuarios
#     """
#     retrieve_permissions = [PermisoUser.view_user.perm]
#     update_permissions = [PermisoUser.change_user.perm]
#     create_permissions = [PermisoUser.add_user.perm]
#     list_permissions = [PermisoUser.view_user.perm]
#     destroy_permissions = [PermisoUser.delete_user.perm]
#     activate_permissions = [PermisoUser.activar_user.perm]
#     inactivate_permissions = [PermisoUser.inactivar_user.perm]
#     UserModel = get_user_model()
#     queryset = UserModel.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     search_fields = ['username', 'first_name', 'last_name', 'email']
#     filter_backends = (filters.SearchFilter,)
#
#     def create(self, request, *args, **kwargs):
#         serializer = PasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         res = super(UserViewSet, self).create(request, *args, **kwargs)
#         user = UserModel.objects.get(pk=res.data['id'])
#         user.set_password(serializer.validated_data['password1'])
#         user.is_active = False
#         user.save()
#         return res
#
#     def update(self, request, *args, **kwargs):
#         serializer = None
#         if 'is_active' in request.data.keys():
#             del request.data['is_active']
#         if 'password1' and 'password2' in request.data.keys():
#             serializer = PasswordSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#         res = super(UserViewSet, self).update(request, *args, **kwargs)
#         if serializer:
#             user = UserModel.objects.get(pk=res.data['id'])
#             user.set_password(serializer.validated_data['password1'])
#             user.save()
#         return res
#
#     @detail_route(methods=['post'])
#     def activar(self, request, pk=None):
#         if not request.user.has_perms(self.activate_permissions):
#             raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
#         instance = self.get_object()
#         if instance.is_active:
#             raise ValidationError(dict(detail=Info.ACTIVO))
#         serializer = self.get_serializer(instance, data={'is_active': True}, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#
#         return Response(dict(message=Success.ACTIVADO), status=status.HTTP_200_OK)
#
#     @detail_route(methods=['post'])
#     def inactivar(self, request, pk=None):
#         if not request.user.has_perms(self.inactivate_permissions):
#             raise ValidationError(dict(detail=Error.NO_TIENE_PERMISO))
#         obj = self.get_object()
#         if not obj.is_active:
#             raise ValidationError(dict(detail=Info.INACTIVO))
#         obj.is_active = False
#         obj.save(update_fields=['is_active'])
#         return Response(dict(message=Success.INACTIVADO), status=status.HTTP_200_OK)

