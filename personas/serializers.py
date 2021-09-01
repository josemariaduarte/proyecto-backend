

from utils.serializers import BaseModelSerializer
from personas.models import Proveedor, Cliente

class ProveedorSerializer(BaseModelSerializer):
    """
    serializer de Proveedor
    """

    class Meta:
        model = Proveedor
        fields = ['id', 'razon_social', 'ruc', 'direccion', 'activo']

    table_columns = ['id', 'razon_social', 'ruc']


class ClienteSerializer(BaseModelSerializer):
    """
    serializer de Proveedor
    """

    class Meta:
        model = Cliente
        fields = ['id', 'nombres', 'apellidos', 'nro_doc', 'fecha_nacimiento',
                  'telefono', 'sexo', 'direccion', 'estado_civil', 'correo', 'activo']

    table_columns = ['id', 'nombres', 'apellidos']