from django.db import models

# Create your models here.
from personas.permissions import PermisoProveedor, PermisoCliente


class Persona(models.Model):
    """
    clase abstracta Persona
    """

    SOLTERO = 1
    CASADO = 2
    DIVORCIADO = 3
    VIUDO = 4
    ESTADO_CIVIL_CHOICES = (
        (SOLTERO, 'SOLTERO'),
        (CASADO, 'CASADO'),
        (DIVORCIADO, 'DIVORCIADO'),
        (VIUDO, 'VIUDO'),
    )
    MASCULINO = 1
    FEMENINO = 2
    SEXO_CHOICES = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino')
    )
    nro_doc = models.CharField('Nro. Documento', max_length=50)
    nombres = models.CharField('Nombres', max_length=150,)
    apellidos = models.CharField('Apellidos', max_length=150)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", blank=True, null=True)
    telefono = models.CharField('Numero de Telefono', max_length=60, blank=True, null=True)
    sexo = models.IntegerField(verbose_name='Sexo', choices=SEXO_CHOICES, default=FEMENINO, blank=True, null=True)
    direccion = models.CharField(verbose_name='Dirección', max_length=255, blank=True, null=True)
    estado_civil = models.IntegerField(choices=ESTADO_CIVIL_CHOICES, verbose_name='Estado Civil', blank=True, null=True)
    correo = models.EmailField(verbose_name='Correo Electronico', blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def get_full_name(self):
        return "%s - %s" % (self.nombres, self.apellidos)


class Cliente(Persona):
    """
    modelo Cliente
    """

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        permissions = PermisoCliente.get_permissions()

    def __str__(self):
        return self.get_full_name()


class Proveedor(models.Model):
    """
    modelo Proveedor
    """

    razon_social = models.CharField(verbose_name='Nombre o Razón Social', max_length=100)
    ruc = models.CharField(verbose_name='RUC', max_length=20)
    direccion = models.CharField(verbose_name='Dirección', max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        permissions = PermisoProveedor.get_permissions()

    def __str__(self):
        return '{} ({})'.format(self.razon_social, self.ruc)

    def save(self, *args, **kwargs):
        self.razon_social = self.razon_social.upper()
        self.direccion = self.direccion.upper()
        self.ruc = self.ruc.upper()
        return super(Proveedor, self).save(*args, **kwargs)
