"""
URLS FOR movimientos
"""

from django.urls import include, path
from rest_framework import routers
from movimientos.views import *

router = routers.DefaultRouter()
router.register(r'orden_compra', OrdenCompraViewSet)
router.register(r'compra', CompraViewSet)
router.register(r'venta', VentaViewSet)
router.register(r'caja', CajaViewSet)
router.register(r'movimiento_caja', MovimientoCajaViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('tipo_comprobante_choices/', get_tipo_comprobante_choices, name='get_tipo_comprobante_choices'),
    path('impuesto_choices/', get_impuesto_choices, name='get_impuesto_choices'),
    path('condicion_choices/', get_condicion_choices, name='get_condicion_choices'),
    path('montos_acumulados_dia/', get_monto_acumulado_dia, name='get_monto_acumulado_dia'),
    path('update_movimientos_by_cierre/', update_movimientos_by_cierre, name='update_movimientos_by_cierre'),
]
