from rest_framework import serializers

from productos.models import SubCategoriaProducto, Categoria, UnidadDeMedida, Deposito, Producto
from utils.serializers import BaseModelSerializer


class CategoriaProductoSerializer(BaseModelSerializer):
    """
    serializer de categorias de productos
    """
    table_columns = ['id', 'nombre']
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'activo']


class SubCategoriaProductoSerializer(BaseModelSerializer):
    """
    serializer de sub categoria de productos
    """
    category_name = serializers.CharField(source='categoria_producto.nombre', required=False)

    class Meta:
        model = SubCategoriaProducto
        fields = ['id', 'nombre', 'descripcion', 'categoria_producto', 'activo', 'category_name']

    table_columns = ['id', 'nombre']


class UnidadDeMedidaSerializer(BaseModelSerializer):
    """
    serializer de unidad de medida
    """
    table_columns = ['id', 'nombre']

    class Meta:
        model = UnidadDeMedida
        fields = ['id', 'nombre', 'descripcion', 'activo']


class DepositoSerializer(BaseModelSerializer):
    """
    serializer de unidad de medida
    """
    table_columns = ['id', 'nombre']

    class Meta:
        model = Deposito
        fields = ['id', 'nombre', 'descripcion', 'direccion', 'activo']


class ProductoSerializer(BaseModelSerializer):
    """
    serializer de unidad de medida
    """
    table_columns = ['id', 'nombre']

    class Meta:
        model = Producto
        fields = ['id',
                  'nombre',
                  'descripcion',
                  'proveedor',
                  'cantidad_minima_stock',
                  'subcategoria',
                  'deposito',
                  'unidad_medida']
