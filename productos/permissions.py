"""
PERMISSIONS FOR Productos
"""
from utils.globals import PermisoEnum


class PermisoSubCategoriaProducto(PermisoEnum):
    activar_subcategoriaproducto = 'Puede Activar SubCategoria Producto'
    inactivar_subcategoriaproducto = 'Puede Inactivar SubCategoria Producto'


PermisoSubCategoriaProducto.app_name = 'productos'


class PermisoCategoriaProducto(PermisoEnum):
    activar_categoriaproducto = 'Puede Activar Categoria Producto'
    inactivar_categoriaproducto = 'Puede Inactivar Categoria Producto'


PermisoCategoriaProducto.app_name = 'productos'


class PermisoArea(PermisoEnum):
    activar_area = 'Puede Activar Area'
    inactivar_area = 'Puede Inactivar Area'


PermisoArea.app_name = 'productos'


class PermisoUnidadDeMedida(PermisoEnum):
    activar_unidaddemedida = 'Puede Activar Unidad de Medida'
    inactivar_unidaddemedida = 'Puede Inactivar Unidad de Medida'


PermisoUnidadDeMedida.app_name = 'productos'


class PermisoDeposito(PermisoEnum):
    activar_deposito = 'Puede Activar Deposito'
    inactivar_deposito = 'Puede Inactivar Deposito'


PermisoDeposito.app_name = 'productos'


class PermisoMarca(PermisoEnum):
    activar_marca = 'Puede Activar Marca'
    inactivar_marca = 'Puede Inactivar Marca'


PermisoMarca.app_name = 'productos'


class PermisoLinea(PermisoEnum):
    activar_linea = 'Puede Activar Linea'
    inactivar_linea = 'Puede Inactivar Linea'


PermisoLinea.app_name = 'productos'


class PermisoProveedor(PermisoEnum):
    activar_linea = 'Puede Activar Proveedor'
    inactivar_linea = 'Puede Inactivar Proveedor'


PermisoProveedor.app_name = 'productos'


class PermisoProducto(PermisoEnum):
    activar_producto = 'Puede Activar Producto'
    inactivar_producto = 'Puede Inactivar Producto'


PermisoProducto.app_name = 'productos'



