"""
URLS FOR movimientos
"""

from django.urls import include, path
from rest_framework import routers
from movimientos.views import *

router = routers.DefaultRouter()
router.register(r'orden_compra', OrdenCompraViewSet)
router.register(r'compra', CompraViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
