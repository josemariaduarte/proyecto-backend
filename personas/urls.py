"""
URLS FOR personas
"""

from django.urls import include, path
from rest_framework import routers
from personas.views import *

router = routers.DefaultRouter()
router.register(r'proveedor', ProveedorViewSet)
router.register(r'cliente', ClienteViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('sexo_choices/', get_sexo_choices, name='get_sexo_choices'),
    path('estado_civil_choices/', get_estado_civil, name='get_estado_choices'),
]
