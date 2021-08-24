from productos.models import SubCategoriaProducto, Categoria
from utils.serializers import BaseModelSerializer


class SubCategoriaProductoSerializer(BaseModelSerializer):
    """
    serializer de sub categoria de productos
    """

    class Meta:
        model = SubCategoriaProducto
        fields = ['id', 'nombre', 'descripcion', 'categoria_producto', 'activo']

    table_columns = ['id', 'nombre']


class CategoriaProductoSerializer(BaseModelSerializer):
    """
    serializer de categorias de productos
    """

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'activo']

    table_columns = ['id', 'nombre']


