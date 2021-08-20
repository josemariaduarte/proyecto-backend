from django.urls import include, path
from rest_framework import routers
from usuarios.views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('token_permissions/', token_permissions, name='token_permissions'),
]
