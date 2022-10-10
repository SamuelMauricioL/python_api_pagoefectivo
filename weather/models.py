from django.db import models


class City(models.Model):
    requestBody = models.CharField(max_length=25)

    def __str__(self):
        return self.requestBody

    class Meta:
        verbose_name_plural = 'cities'


class Configuration(models.Model):
    ServidorPagoEfectivo = models.CharField(max_length=25, default='')
    AccessKey = models.CharField(max_length=25, default='')
    SecretKey = models.CharField(max_length=25, default='')
    IDComercio = models.CharField(max_length=25, default='')
    NombreComercio = models.CharField(max_length=25, default='')
    EmailComercio = models.CharField(max_length=25, default='')
    ModoIntegracion = models.CharField(max_length=25, default='')
    TiempoExpiracionPago = models.CharField(max_length=25, default='')
    Pais = models.CharField(max_length=25, default='')
    TipoMoneda = models.CharField(max_length=25, default='')
    Monto = models.CharField(max_length=25, default='')

    def __str__(self):
        return self


class Notification(models.Model):
    requestBody = models.CharField(max_length=500, default='')
    signature = models.CharField(max_length=200, default='')

    def __str__(self):
        return self


class BodyValidation(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return '%s %s' % (self.title, self.body)
