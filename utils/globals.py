from enum import Enum


class PermisoEnum(Enum):

    @property
    def perm(self):
        """ Retorna el permiso en este formato 'app_name.permission_name'
              Ejemplo:
                uso: PermisoAutorizacion.crear_autorizacion.perm

                Return:
                string: 'usuarios.crear_autorizacion'
        """
        return '%s.%s' % (self.app_name, self.name)

    @classmethod
    def get_permissions(cls):
        """ Retorna la lista de permisos para poder definirlos en el modelo en la clase Meta

            Return:
                List(tuple): [('<permission_code>','<permission_name>'),
                                ('<permission2_code>','<permission2_name>')]
        """
        permissions = []
        for name, member in cls.__members__.items():
            permissions.append((name, member.value))
        return permissions
