

class Error:
    NO_TIENE_PERMISO: str = 'Usted no tiene permiso para realizar esta acción.'
    CAMPOS_CONTRASENHA: str = 'Los dos campos de contraseña no coinciden.'
    NO_TIENE_CAMPO_ACTIVO: str = 'No tiene el campo activo.'
    CAMPO_NULO: str = 'la clase {serializer_class} no tiene un valor en el campo "{campo}"'


class Info:
    ACTIVO: str = 'Ya se encuentra  Activo.'
    INACTIVO: str = 'Ya se encuentra Inactivo.'


class Success:
    ACTIVADO: str = 'Registro activado correctamente.'
    INACTIVADO: str = 'Registro inactivado correctamente.'
    ORDEN_APROBADO: str = 'Orden de Compra Aprobado'
    ORDEN_RECHAZADO: str = 'Orden de Compra Rechazado'

