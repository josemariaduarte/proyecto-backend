"""
PERMISSIONS FOR Productos
"""
from utils.globals import PermisoEnum


class PermisoProveedor(PermisoEnum):
    activar_proveedor = 'Puede Activar Proveedor'
    inactivar_proveedor = 'Puede Inactivar Proveedor'


PermisoProveedor.app_name = 'personas'



