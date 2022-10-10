from django.forms import ModelForm, TextInput
from django import forms
from .models import Notification, Configuration

class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['requestBody', 'signature']
        widgets = {
            'requestBody' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
            'signature' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"})
            }


class ConfigurationForm(ModelForm):
    class Meta:
        model = Configuration 
        fields = ['ServidorPagoEfectivo',
                  'AccessKey',
                  'SecretKey',
                  'IDComercio',
                  'NombreComercio',
                  'EmailComercio',
                  'ModoIntegracion',
                  'TiempoExpiracionPago',
                  'Pais',
                  'TipoMoneda',
                  'Monto'
                  ]
        widgets = {
                    'ServidorPagoEfectivo' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'AccessKey' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'SecretKey' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'IDComercio' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'NombreComercio' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'EmailComercio' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'ModoIntegracion' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'TiempoExpiracionPago' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'TipoMoneda' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'Monto' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden"}),
                    'Pais' : TextInput(attrs={'class' : 'input hidden', "type" : "hidden", 'onchange':'handleCountry();'})
                    }