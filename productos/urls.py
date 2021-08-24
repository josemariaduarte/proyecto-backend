"""
URLS FOR productos
"""

from django.urls import include, path
from rest_framework import routers
from productos.views import *

router = routers.DefaultRouter()
router.register(r'sub_categoria_producto', SubCategoriaProductoViewSet)
router.register(r'categoria_producto', CategoriaProductoViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
