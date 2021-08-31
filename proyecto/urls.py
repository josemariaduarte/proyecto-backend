"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuarios.views import my_token_pair_view
from rest_framework_simplejwt.views import token_verify, token_refresh

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/v1/token/', my_token_pair_view, name='token_obtain_pair'),
    path('api/v1/token/refresh/', token_refresh, name='token_refresh'),
    path('api/v1/token/verify/', token_verify, name='token_verify'),

    # MODULOS
    path('api/v1/usuarios/', include('usuarios.urls')),
    path('api/v1/productos/', include('productos.urls')),
    path('api/v1/personas/', include('personas.urls')),

]
