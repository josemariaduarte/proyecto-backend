"""
URLS FOR productos
"""

from django.urls import include, path
from rest_framework import routers
from productos.views import *

router = routers.DefaultRouter()
router.register(r'sub_categoria', SubCategoriaProductoViewSet)
router.register(r'categoria', CategoriaProductoViewSet)
router.register(r'unidad_medida', UnidadMedidaViewSet)
router.register(r'deposito', DepositoViewSet)
router.register(r'articulo', ProductoViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
