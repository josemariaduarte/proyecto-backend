from rest_framework import serializers

from productos.models import SubCategoriaProducto, Categoria
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




