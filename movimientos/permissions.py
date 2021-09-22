"""
PERMISSIONS FOR Productos
"""
from utils.globals import PermisoEnum


class PermisoOrdenCompra(PermisoEnum):
    activar_orden_compra = 'Puede Activar Orden Compra'
    inactivar_orden_compra = 'Puede Inactivar Orden Compra'


PermisoOrdenCompra.app_name = 'movimientos'
