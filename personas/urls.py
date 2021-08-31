"""
URLS FOR personas
"""

from django.urls import include, path
from rest_framework import routers
from personas.views import *

router = routers.DefaultRouter()
router.register(r'proveedor', ProveedorViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
