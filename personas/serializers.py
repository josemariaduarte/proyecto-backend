

from utils.serializers import BaseModelSerializer
from personas.models import Proveedor

class ProveedorSerializer(BaseModelSerializer):
    """
    serializer de Proveedor
    """

    class Meta:
        model = Proveedor
        fields = ['id', 'razon_social', 'ruc', 'direccion', 'activo']

    table_columns = ['id', 'razon_social', 'ruc']
