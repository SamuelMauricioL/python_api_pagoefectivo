import requests
from django.shortcuts import render
from .models import City, Notification
from .forms import ConfigurationForm, NotificationForm
import http.client
import json
from django.http import HttpResponseRedirect, HttpResponse
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
import time
import hmac
import hashlib
import os
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
import pytz
import re
from django.utils import timezone
# djangorest framework
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.template.loader import get_template

# FUNCION PARA GENERAR O HOME "/"
@csrf_exempt
def index(request):
    tZ = "America/Lima"
    bdyAh = {}
    bdC = {}
    ctryLoaded = ""
    montoLoaded = ""
    currencyLoaded = ""
    AcssKyLded = ""
    sctrKyLded = ""
    idComLded = ""
    timeExpiration = 0
    esPostBack = 0
    emailLoaded = ""
    auxMontGenerate = ""
    modoIntgonLded = ""
    urlServerLoaded = ""
    auxMoun = 0
    disabledButton = True
    if request.COOKIES.get('ServidorPagoEfectivo'):
        urlServerLoaded = request.COOKIES['ServidorPagoEfectivo']

    if request.COOKIES.get('ModoIntegracion'):
        modoIntgonLded = request.COOKIES['ModoIntegracion']

    if request.COOKIES.get('pais'):
        ctryLoaded = request.COOKIES['pais']

    if request.COOKIES.get('TipoMoneda'):
        currencyLoaded = request.COOKIES['TipoMoneda']

    if request.COOKIES.get('Monto'):
        montoLoaded = request.COOKIES['Monto']

    if request.COOKIES.get('NombreComercio'):
        NombreComercioLoaded = request.COOKIES['NombreComercio']

    if request.COOKIES.get('EmailComercio'):
        emailLoaded = request.COOKIES['EmailComercio']

    if request.COOKIES.get('AccessKey'):
        AcssKyLded = request.COOKIES['AccessKey']

    if request.COOKIES.get('SecretKey'):
        sctrKyLded = request.COOKIES['SecretKey']

    if request.COOKIES.get('IDComercio'):
        idComLded = request.COOKIES['IDComercio']

    if request.COOKIES.get('TiempoExpiracionPago'):
        timeExpiration = request.COOKIES['TiempoExpiracionPago']

    auxMoun = re.sub(r"^(-?\d+)(\d{3})", r"\g<1>,\g<2>", montoLoaded)

    if montoLoaded:
        auxMontGenerate = str(auxMoun)
    else:
        auxMontGenerate = ""

    if request.method == "GET":
        if (modoIntgonLded and
                montoLoaded and
                ctryLoaded and
                currencyLoaded and
                NombreComercioLoaded and
                emailLoaded and
                AcssKyLded and
                sctrKyLded and
                idComLded and
                timeExpiration and
                urlServerLoaded):
            disabledButton = False

        context = {
            "esPostBack": esPostBack,
            "country": ctryLoaded,
            "montoFromConfg": auxMontGenerate,
            "currencyLoaded": currencyLoaded,
            "disabledButton": disabledButton
        }
        response = render(request, 'weather/weather.html', context)
        return response

    if request.method == 'POST':
        if request.POST.get("btnGuardar"):

            # HORA EXACTA DE LA GENERACION DEL PROCESO
            dateNowAddTimeToExp = datetime.now((pytz.timezone(tZ)))
            cutDateNowAddTimeToExp = str(dateNowAddTimeToExp)
            cutDateNowAddTimeToExp = cutDateNowAddTimeToExp.replace('.', " ")
            aux = cutDateNowAddTimeToExp.split(' ')
            dtFlFmtd = aux[0] + "T" + aux[1] + "-05:00"

            # CONVERSION DE FECHA A FORMATO ATOM (AMERICA/LATINA)
            hsAdd = int(timeExpiration)
            dtExp = datetime.now((pytz.timezone(tZ))) + timedelta(hours=hsAdd)
            cutDtyNowAddTimeToExp = str(dtExp)
            cutDtyNowAddTimeToExp = cutDtyNowAddTimeToExp.replace('.', " ")
            auxExpiry = cutDtyNowAddTimeToExp.split(' ')
            dtExpFinalFormated = auxExpiry[0] + "T" + auxExpiry[1] + "-05:00"
            ####

            auxMont = str(montoLoaded)

            # GENERACION DE HASH sha256 PARA CABECERA
            strCom = str(idComLded)
            hsh = strCom + "." + AcssKyLded + "." + sctrKyLded + "." + dtFlFmtd
            hsh = hsh.encode('utf-8')
            hash_object = hashlib.sha256(hsh).hexdigest()
            ######

            bdyAh = {
                    "accessKey": AcssKyLded,
                    "idService": int(idComLded),
                    "dateRequest": dtFlFmtd,
                    "hashString": hash_object
                    }

            if bdyAh:
                headers_data = {
                    'Content-Type': 'application/json; charset=UTF-8',
                }
                # LLAMADA AL SERVICIO /AUTHORIZATIONS
                rA = 'https://pre1a.services.pagoefectivo.pe/v1/authorizations'
                response = requests.post(rA, json=bdyAh, headers=headers_data)
                print(response.status_code, "response.status_code AUTH")
                responseAuthJson = response.json()
                if response.status_code == 201:
                    print("201 Auth")
                    if responseAuthJson["code"] == 100:
                        print(responseAuthJson, "resAuthJson AUTH & TOKEN")
                        tokenAux = responseAuthJson["data"]["token"]

                        hdrCip = {
                            'Content-Type': 'application/json; charset=UTF-8',
                            'Accept-Language': 'es-PE',
                            'Authorization': 'Bearer' + " " + tokenAux
                            }
                        ecu = "ECUADOR"
                        pe = "PERU"
                        bdC = {
                            "currency": currencyLoaded,
                            "amount": auxMont,
                            "transactionCode": "208",
                            "dateExpiry": dtExpFinalFormated,
                            "paymentConcept": "Prueba 200",
                            "additionalData": "datos adicionales de prueba",
                            "userEmail": emailLoaded,
                            "adminEmail": emailLoaded,
                            "userId": 200,
                            "userName": "Chester",
                            "userLastName": "Alvarado",
                            "userUbigeo": 150101,
                            "userCountry": pe if ctryLoaded == "PER" else ecu,
                            "userDocumentType": "DNI",
                            "userDocumentNumber": "40226700",
                            "userCodeCountry": "+51",
                            "userPhone": "9988776650",
                            "serviceId": int(idComLded)
                        }
                        # LLAMADA AL SERVICIO /CIPS
                        rtC = 'https://pre1a.services.pagoefectivo.pe/v1/cips'
                        rsCip = requests.post(rtC, json=bdC, headers=hdrCip)
                        print(rsCip.status_code, "status_code /cips")
                        rsCipJson = rsCip.json()
                        if rsCip.status_code == 201:
                            print("201 Cips")
                            if rsCipJson["code"] == 100:
                                esPostBack = 1
                                amountByService = rsCipJson["data"]["amount"]
                                enalceCip = rsCipJson["data"]["cipUrl"]
                                context = {
                                    "modoIntegrationLoaded": modoIntgonLded,
                                    "country": ctryLoaded,
                                    "currencyLoaded": currencyLoaded,
                                    "montoFromConfg": amountByService,
                                    "enlaceCIP": enalceCip,
                                    "esPostBack": esPostBack
                                }
                                htmlFile = 'weather/weather.html'
                                response = render(request, htmlFile, context)
                                # ALMACENAMIENTO DE VARIABLES EN MEMORIA
                                response.set_cookie('token', tokenAux)
                                cipAux = rsCipJson["data"]["cip"]
                                response.set_cookie('cipAuth', cipAux)
                                cipUrl = rsCipJson["data"]["cipUrl"]
                                response.set_cookie('cipUrlAuth', cipUrl)
                                cipM = rsCipJson["data"]["amount"]
                                response.set_cookie('amountAuth', cipM)
                                cipCrr = rsCipJson["data"]["currency"]
                                response.set_cookie('penAuth', cipCrr)

                                if modoIntgonLded == "RED":
                                    return HttpResponseRedirect(enalceCip)
                                else:
                                    return response
                        else:
                            print("NO SE GENERO CIP")
                            context = {
                                "country": ctryLoaded,
                                "montoFromConfg": auxMontGenerate,
                                "currencyLoaded": currencyLoaded,
                                "esPostBack": esPostBack
                            }
                            htmlFile = 'weather/weather.html'
                            response = render(request, htmlFile, context)
                            return response
                else:
                    print("No genero autorizacion ni TOKEN")
                    context = {
                        "country": ctryLoaded,
                        "montoFromConfg": auxMontGenerate,
                        "currencyLoaded": currencyLoaded,
                        "esPostBack": esPostBack
                    }
                    htmlFile = 'weather/weather.html'
                    response = render(request, htmlFile, context)
                    return response

    context = {
        "country": ctryLoaded,
        "montoFromConfg": auxMontGenerate,
        "currencyLoaded": currencyLoaded
    }
    htmlFile = 'weather/weather.html'
    return render(request, htmlFile, context)

# FUNCION PARA /NOTIFICATION
@csrf_exempt
def indexNotification(request):
    isSaved = "0"
    currencyLoaded = ""
    montoLoaded = ""
    secretKeyLoaded = ""
    form = ""
    amountByService = 0
    cipByService = 0
    emptySignature = ""
    emptyRqBody = ""
    value1 = ""
    value2 = ""
    cleanBody = False

    if request.method == "GET":
        if request.COOKIES.get('penAuth'):
            currencyLoaded = request.COOKIES['penAuth']

        if request.COOKIES.get('Monto'):
            montoLoaded = request.COOKIES['Monto']

        if request.COOKIES.get('amountAuth'):
            amountByService = request.COOKIES['amountAuth']

        if request.COOKIES.get('cipAuth'):
            cipByService = request.COOKIES['cipAuth']

            context = {
                "key_filed": isSaved,
                "currencyFromConfig": currencyLoaded,
                "montoFromConfig": amountByService,
                "cipByService": cipByService
            }
            return render(request, 'weather/notification.html', context)

    if request.method == "POST":
        if request.POST.get("btnLimpiar"):
            cleanBody = True
            context = {"cleanBody": cleanBody}
            return render(request, 'weather/notification.html', context)

        form = NotificationForm(request.POST)

        aux1 = str(form.__getitem__('requestBody'))
        aux2 = str(form.__getitem__('signature'))

        soup = BeautifulSoup(aux1)
        soup2 = BeautifulSoup(aux2)

        value1 = soup.find('input').get('value')
        value2 = soup2.find('input').get('value')

        if value1 and value2:
            if not value1:
                emptySignature = "2"

            if not value2:
                emptyRqBody = "2"

            if request.COOKIES.get('penAuth'):
                currencyLoaded = request.COOKIES['penAuth']

            if request.COOKIES.get('amountAuth'):
                montoLoaded = request.COOKIES['amountAuth']

            if request.COOKIES.get('SecretKey'):
                secretKeyLoaded = request.COOKIES['SecretKey']

            aux1 = str(form.__getitem__('requestBody'))
            aux2 = str(form.__getitem__('signature'))

            parse1 = BeautifulSoup(aux1)
            parse2 = BeautifulSoup(aux2)

            value1 = parse1.find('input').get('value')
            value2 = parse2.find('input').get('value')
            body = {
                'PE-Signature': value2,
                'requestBody': value1
            }

            signatureAux = body["PE-Signature"]
            rqBody = body["requestBody"]
            strSkL = str(secretKeyLoaded)
            ln = 'latin-1'
            hshLib = hashlib.sha256
            varBytes = bytes(strSkL, ln)
            sgn = hmac.new(varBytes, msg=bytes(rqBody, ln), digestmod=hshLib)
            signatureHex = sgn.hexdigest()
            signatureAux = body["PE-Signature"]

            if signatureHex == str(signatureAux):
                form.save()
                isSaved = "1"
                emptyField = ""
                context = {
                    "form": form,
                    "key_filed": isSaved,
                    "emptyField": emptyField,
                    "currencyFromConfig": currencyLoaded,
                    "montoFromConfig": montoLoaded
                }
                return render(request, 'weather/notification.html', context)
            else:
                form.save()
                isSaved = "2"
                context = {
                    "form": form,
                    "key_filed": isSaved,
                    "montoFromConfig": montoLoaded,
                    "currencyFromConfig": currencyLoaded
                }
                return render(request, 'weather/notification.html', context)
        else:
            if not value1:
                emptyRqBody = "1"

            if not value2:
                emptySignature = "1"

            context = {
                "form": form,
                "key_filed": isSaved,
                "emptyRq": emptyRqBody,
                "emptySigt": emptySignature
            }
            return render(request, 'weather/notification.html', context)

    context = {'form': form, 'key_filed': isSaved}
    return render(request, 'weather/notification.html', context)

# FUNCION PARA /CONFIGURATION
@csrf_exempt
def indexConfiguration(request):
    isSaved = "0"
    form = ""
    form2 = ""
    ctryLoaded = ""
    ModoIntegracionLoaded = ""
    TipoMonedaLoaded = ""
    ServidorPagoEfectivoLoaded = ""
    AcssKyLded = ""
    sctrKyLded = ""
    idComLded = ""
    NombreComercioLoaded = ""
    EmailComercioLoaded = ""
    MontoLoaded = ""
    TiempoExpiracionPagoLoaded = ""
    TipoMonedaLoaded = ""
    value1 = ""
    value2 = ""
    value3 = ""
    value4 = ""
    value5 = ""
    value6 = ""
    value7 = ""
    value8 = ""
    value9 = ""
    value10 = ""
    value11 = ""
    # VALUES FOR FIELDS VALIDATION
    empty1 = ""
    empty2 = ""
    empty3 = ""
    empty4 = ""
    empty5 = ""
    empty6 = ""
    empty7 = ""
    empty8 = ""
    empty9 = ""
    empty10 = ""
    empty11 = ""

    if request.COOKIES.get('pais'):
        ctryLoaded = request.COOKIES['pais']

    if request.COOKIES.get('ServidorPagoEfectivo'):
        ServidorPagoEfectivoLoaded = request.COOKIES['ServidorPagoEfectivo']

    if request.COOKIES.get('AccessKey'):
        AcssKyLded = request.COOKIES['AccessKey']

    if request.COOKIES.get('SecretKey'):
        sctrKyLded = request.COOKIES['SecretKey']

    if request.COOKIES.get('IDComercio'):
        idComLded = request.COOKIES['IDComercio']

    if request.COOKIES.get('NombreComercio'):
        NombreComercioLoaded = request.COOKIES['NombreComercio']

    if request.COOKIES.get('EmailComercio'):
        EmailComercioLoaded = request.COOKIES['EmailComercio']

    if request.COOKIES.get('Monto'):
        MontoLoaded = request.COOKIES['Monto']

    if request.COOKIES.get('TiempoExpiracionPago'):
        TiempoExpiracionPagoLoaded = request.COOKIES['TiempoExpiracionPago']

    if request.COOKIES.get('TipoMoneda'):
        TipoMonedaLoaded = request.COOKIES['TipoMoneda']

    if request.COOKIES.get('ModoIntegracion'):
        ModoIntegracionLoaded = request.COOKIES['ModoIntegracion']

    if request.method == 'POST':
        if request.POST.get("btnCancelar"):
            print("LIMPIAR CONFIG")
            form = ""
            context = {
                'form': form,
                "countryLoaded": "",
                "ServidorPagoEfectivoLoaded": "",
                "AccessKeyLoaded": "",
                "SecretKeyLoaded": "",
                "IDComercioLoaded": "",
                "NombreComercioLoaded": "",
                "EmailComercioLoaded": "",
                "MontoLoaded": "",
                "TiempoExpiracionPagoLoaded": "",
                "TipoMonedaLoaded": "",
                "ModoIntegracionLoaded": ""
            }
            return render(request, 'weather/configuration.html', context)

    if request.method == "GET":
        request.COOKIES.get('form')

        if request.COOKIES.get('form'):
            formLoaded = request.COOKIES['form']

        context = {
            "countryLoaded": ctryLoaded,
            "ServidorPagoEfectivoLoaded": ServidorPagoEfectivoLoaded,
            "AccessKeyLoaded": AcssKyLded,
            "SecretKeyLoaded": sctrKyLded,
            "IDComercioLoaded": idComLded,
            "NombreComercioLoaded": NombreComercioLoaded,
            "EmailComercioLoaded": EmailComercioLoaded,
            "MontoLoaded": MontoLoaded,
            "TiempoExpiracionPagoLoaded": TiempoExpiracionPagoLoaded,
            "TipoMonedaLoaded": TipoMonedaLoaded,
            "ModoIntegracionLoaded": ModoIntegracionLoaded
                }
        return render(request, 'weather/configuration.html', context)

    if request.method == 'POST':
        form2 = ConfigurationForm(request.POST)
        aux1 = str(form2.__getitem__('ServidorPagoEfectivo'))
        aux2 = str(form2.__getitem__('AccessKey'))
        aux3 = str(form2.__getitem__('SecretKey'))
        aux4 = str(form2.__getitem__('IDComercio'))
        aux5 = str(form2.__getitem__('NombreComercio'))
        aux6 = str(form2.__getitem__('EmailComercio'))
        aux8 = str(form2.__getitem__('TiempoExpiracionPago'))
        aux11 = str(form2.__getitem__('Monto'))
        aux7 = str(form2.__getitem__('ModoIntegracion'))
        aux9 = str(form2.__getitem__('Pais'))
        aux10 = str(form2.__getitem__('TipoMoneda'))

        soup = BeautifulSoup(aux1)
        soup2 = BeautifulSoup(aux2)
        soup3 = BeautifulSoup(aux3)
        soup4 = BeautifulSoup(aux4)
        soup5 = BeautifulSoup(aux5)
        soup6 = BeautifulSoup(aux6)
        soup8 = BeautifulSoup(aux8)
        soup11 = BeautifulSoup(aux11)
        soup7 = BeautifulSoup(aux7)
        soup9 = BeautifulSoup(aux9)
        soup10 = BeautifulSoup(aux10)

        value1 = soup.find('input').get('value')
        value2 = soup2.find('input').get('value')
        value3 = soup3.find('input').get('value')
        value4 = soup4.find('input').get('value')
        value5 = soup5.find('input').get('value')
        value6 = soup6.find('input').get('value')
        value8 = soup8.find('input').get('value')
        value11 = soup11.find('input').get('value')
        value7 = soup7.find('input').get('value')
        value9 = soup9.find('input').get('value')
        value10 = soup10.find('input').get('value')

        if not value9:
            if request.COOKIES.get('pais'):
                value9 = request.COOKIES['pais']

        if not value7:
            if request.COOKIES.get('ModoIntegracion'):
                value7 = request.COOKIES['ModoIntegracion']

        if not value10:
            if request.COOKIES.get('TipoMoneda'):
                value10 = request.COOKIES['TipoMoneda']

        if (value1 and value2 and
                value3 and value4 and
                value5 and value6 and
                value7 and value8 and
                value9 and value10 and
                value11):

            body = {
                    "ServidorPagoEfectivo": value1,
                    "AccessKey": value2,
                    "SecretKey": value3,
                    "IDComercio": value4,
                    "NombreComercio": value5,
                    "EmailComercio": value6,
                    "ModoIntegracion": value7,
                    "TiempoExpiracionPago": value8,
                    "Pais": value9,
                    "TipoMoneda": value10,
                    "Monto": value11
            }
            if body:
                pth = os.path.abspath(os.path.dirname(__file__))
                with open(pth + '/static/cadmin/config.json') as f:
                    data = json.load(f)

                    print(data, "data")
                    data['SecretKey'] = value3

                with open(pth + '/static/cadmin/configSaved.json', 'w') as f:
                    json.dump(data, f)

                isSaved = "1"
                context = {
                    "form": form2,
                    "key_filed": isSaved,
                    "countryLoaded": value9,
                    "TipoMonedaLoaded": value10,
                    "ModoIntegracionLoaded": value7
                }
                htmlConf = "weather/configuration.html"
                response = render(request, htmlConf, context)
                response.set_cookie('form', form2)
                response.set_cookie('pais', value9)
                response.set_cookie('ServidorPagoEfectivo', value1)
                response.set_cookie('AccessKey', value2)
                response.set_cookie('SecretKey', value3)
                response.set_cookie('IDComercio', value4)
                response.set_cookie('NombreComercio', value5)
                response.set_cookie('EmailComercio', value6)
                response.set_cookie('ModoIntegracion', value7)
                auxMont1 = str(value11)
                if auxMont1.find(".") != -1:
                    splitMount = auxMont1.split(".")
                    charctsMount = len(splitMount[1])
                    # VALIDACION DE CANTIDAD DE DECIMALES,
                    #  SI TIENE UN DECIMAL, SE AUTOCOMPLETARA CON UN 0 AL FINAL
                    if charctsMount == 1:
                        auxMont1 = auxMont1 + "0"
                else:
                    auxMont1 = auxMont1 + ".00"
                response.set_cookie('Monto', auxMont1)
                response.set_cookie('TiempoExpiracionPago', value8)
                response.set_cookie('TipoMoneda', value10)
                return response
            else:
                form2.save()
                isSaved = "2"
                context = {'form': form2, 'key_filed': isSaved}
                return render(request, 'weather/configuration.html', context)
        else:
            if not value1:
                empty1 = "1"

            if not value2:
                empty2 = "1"

            if not value3:
                empty3 = "1"

            if not value4:
                empty4 = "1"

            if not value5:
                empty5 = "1"

            if not value6:
                empty6 = "1"

            if not value7:
                empty7 = "1"

            if not value8:
                empty8 = "1"

            if not value9:
                empty9 = "1"

            if not value10:
                empty10 = "1"

            if not value11:
                empty11 = "1"

            context = {
                'form': form2,
                'key_filed': isSaved,
                "empty1": empty1,
                "empty2": empty2,
                "empty3": empty3,
                "empty4": empty4,
                "empty5": empty5,
                "empty6": empty6,
                "empty8": empty8,
                "empty10": empty10,
                "empty7": empty7,
                "empty11": empty11,
                "empty9": empty9
            }
            return render(request, 'weather/configuration.html', context)

        if ((value1 and value2 and
                value3 and value4 and
                value5 and value6 and
                value7 and value8 and
                value9 and value10 and
                value11) is not True or
                ctryLoaded or ModoIntegracionLoaded or
                TipoMonedaLoaded):
            aux1 = str(form2.__getitem__('ServidorPagoEfectivo'))
            aux2 = str(form2.__getitem__('AccessKey'))
            aux3 = str(form2.__getitem__('SecretKey'))
            aux4 = str(form2.__getitem__('IDComercio'))
            aux5 = str(form2.__getitem__('NombreComercio'))
            aux6 = str(form2.__getitem__('EmailComercio'))
            aux8 = str(form2.__getitem__('TiempoExpiracionPago'))
            aux11 = str(form2.__getitem__('Monto'))
            aux7 = str(form2.__getitem__('ModoIntegracion'))
            aux9 = str(form2.__getitem__('Pais'))
            aux10 = str(form2.__getitem__('TipoMoneda'))

            soup = BeautifulSoup(aux1)
            soup2 = BeautifulSoup(aux2)
            soup3 = BeautifulSoup(aux3)
            soup4 = BeautifulSoup(aux4)
            soup5 = BeautifulSoup(aux5)
            soup6 = BeautifulSoup(aux6)
            soup8 = BeautifulSoup(aux8)
            soup11 = BeautifulSoup(aux11)
            soup7 = BeautifulSoup(aux7)
            soup9 = BeautifulSoup(aux9)
            soup10 = BeautifulSoup(aux10)

            value1 = soup.find('input').get('value')
            value2 = soup2.find('input').get('value')
            value3 = soup3.find('input').get('value')
            value4 = soup4.find('input').get('value')
            value5 = soup5.find('input').get('value')
            value6 = soup6.find('input').get('value')
            value8 = soup8.find('input').get('value')
            value11 = soup11.find('input').get('value')
            value7 = soup7.find('input').get('value')
            value9 = soup9.find('input').get('value')
            value10 = soup10.find('input').get('value')

            body = {
                    "ServidorPagoEfectivo": value1,
                    "AccessKey": value2,
                    "SecretKey": value3,
                    "IDComercio": value4,
                    "NombreComercio": value5,
                    "EmailComercio": value6,
                    "ModoIntegracion": value7,
                    "TiempoExpiracionPago": value8,
                    "Pais": value9,
                    "TipoMoneda": value10,
                    "Monto": value11
            }
            if body:
                isSaved = "1"
                aux1 = str(form2.__getitem__('ServidorPagoEfectivo'))
                aux2 = str(form2.__getitem__('AccessKey'))
                aux3 = str(form2.__getitem__('SecretKey'))
                aux4 = str(form2.__getitem__('IDComercio'))
                aux5 = str(form2.__getitem__('NombreComercio'))
                aux6 = str(form2.__getitem__('EmailComercio'))
                aux7 = str(form2.__getitem__('TiempoExpiracionPago'))
                aux8 = str(form2.__getitem__('Monto'))
                aux9 = str(form2.__getitem__('Pais'))
                aux10 = str(form2.__getitem__('TipoMoneda'))
                aux11 = str(form2.__getitem__('ModoIntegracion'))

                parse1 = BeautifulSoup(aux1)
                parse2 = BeautifulSoup(aux2)
                parse3 = BeautifulSoup(aux3)
                parse4 = BeautifulSoup(aux4)
                parse5 = BeautifulSoup(aux5)
                parse6 = BeautifulSoup(aux6)
                parse7 = BeautifulSoup(aux7)
                parse8 = BeautifulSoup(aux8)
                parse9 = BeautifulSoup(aux9)
                parse10 = BeautifulSoup(aux10)
                parse11 = BeautifulSoup(aux11)

                value1 = parse1.find('input').get('value')
                value2 = parse2.find('input').get('value')
                value3 = parse3.find('input').get('value')
                value4 = parse4.find('input').get('value')
                value5 = parse5.find('input').get('value')
                value6 = parse6.find('input').get('value')
                value7 = parse7.find('input').get('value')
                value8 = parse8.find('input').get('value')
                value9 = parse9.find('input').get('value')
                value10 = parse10.find('input').get('value')
                value11 = parse11.find('input').get('value')

                # GRABAR secretKey archivoConfig
                pth = os.path.abspath(os.path.dirname(__file__))
                with open(pth + '/static/cadmin/config.json') as f:
                    data = json.load(f)

                    print(data, "data")
                    data['SecretKey'] = value3

                with open(pth + '/static/cadmin/configSaved.json', 'w') as f:
                    json.dump(data, f)
                modoLded = value11 if value11 else ModoIntegracionLoaded
                tipoMnedLded = value10 if value10 else TipoMonedaLoaded
                context = {
                    'key_filed': isSaved,
                    "ServidorPagoEfectivoLoaded": value1,
                    "AccessKey": value2,
                    "sctrKyLded": value3,
                    "IDComercio": value4,
                    "NombreComercioLoaded": value5,
                    "EmailComercioLoaded": value6,
                    "TiempoExpiracionPagoLoaded": value7,
                    "ModoIntegracionLoaded": modoLded,
                    "MontoLoaded": value8,
                    "countryLoaded": value9 if value9 else ctryLoaded,
                    "TipoMonedaLoaded": tipoMnedLded
                }
                htmlConf = 'weather/configuration.html'
                response = render(request, htmlConf, context)
                response.set_cookie('ServidorPagoEfectivo', value1)
                response.set_cookie('AccessKey', value2)
                response.set_cookie('SecretKey', value3)
                response.set_cookie('IDComercio', value4)
                response.set_cookie('NombreComercio', value5)
                response.set_cookie('EmailComercio', value6)
                response.set_cookie('TiempoExpiracionPago', value7)
                auxMont1 = float(value8)
                auxMont1 = "{:.2f}".format(auxMont1)
                response.set_cookie('Monto', str(auxMont1))

                if value9:
                    response.set_cookie('pais', value9)
                else:
                    response.set_cookie('pais', ctryLoaded)

                if value10:
                    response.set_cookie('TipoMoneda', value10)
                else:
                    response.set_cookie('TipoMoneda', TipoMonedaLoaded)

                mdoLoaded = ModoIntegracionLoaded

                if value11:
                    response.set_cookie('ModoIntegracion', value11)
                else:
                    response.set_cookie('ModoIntegracion', mdoLoaded)
                return response
            else:
                isSaved = "2"
                context = {
                    'key_filed': isSaved,
                    "ServidorPagoEfectivoLoaded": ServidorPagoEfectivoLoaded,
                    "AccessKeyLoaded": AcssKyLded,
                    "SecretKeyLoaded": sctrKyLded,
                    "IDComercioLoaded": idComLded,
                    "NombreComercioLoaded": NombreComercioLoaded,
                    "EmailComercioLoaded": EmailComercioLoaded,
                    "MontoLoaded": MontoLoaded,
                    "TiempoExpiracionPagoLoaded": TiempoExpiracionPagoLoaded,
                    "TipoMonedaLoaded": TipoMonedaLoaded,
                    "ModoIntegracionLoaded": ModoIntegracionLoaded,
                    "countryLoaded": ctryLoaded
                }
                return render(request, 'weather/configuration.html', context)

    context = {
        'form': form2,
        'key_filed': isSaved,
        "countryLoaded": ctryLoaded,
        "ModoIntegracionLoaded": ModoIntegracionLoaded,
        "TipoMonedaLoaded": TipoMonedaLoaded
    }
    return render(request, 'weather/configuration.html', context)

# FUNCION PARA /VALIDATION DESDE POSTMAN "/validation"
@api_view(["GET", "POST"])
def IdealWeight(request):
    if request.method == "GET":
        template = get_template("weather/empty.html")
        return HttpResponse(template.render(), status=500)

    if request.method == 'POST':
        signatureReceived = str(request.META.get("HTTP_PE_SIGNATURE"))
        pth = os.path.abspath(os.path.dirname(__file__))
        json_data = open(pth + '/static/cadmin/configSaved.json')
        data1 = json.load(json_data)
        json_data.close()

        if signatureReceived:
            amountReplaced = ""
            secretKeyLoadedConfig = data1["SecretKey"]
            body = json.loads(request.body)
            amountReceive = body['data']['amount']
            auxMont = amountReceive
            auxMont1 = str(amountReceive)

            if auxMont1.find(".") != -1:
                splitMount = auxMont1.split(".")
                charctsMount = len(splitMount[1])
                # VALIDACION DE CANTIDAD DE DECIMALES,
                #  SI TIENE UN DECIMAL, SE AUTOCOMPLETARA CON UN 0 AL FINAL
                if charctsMount == 1:
                    auxMont = auxMont1 + "0"
                    amountReplaced = auxMont
                else:
                    auxMont = auxMont
                body['data']['amount'] = auxMont
            else:
                amountReplaced = auxMont1 + ".00"
                body['data']['amount'] = amountReplaced

            bodyRpl = str(body).replace("'", '"')
            bodyAux = {
                "req": bodyRpl.replace(" ", "").replace(" ", "")
            }

            bdA = bodyAux['req']

            if (amountReplaced):
                arrayAmount = amountReplaced.split(".")
                part1 = 'amount":"' + arrayAmount[0] + "."
                part1Fix = 'amount":' + arrayAmount[0] + "."
                part2 = "." + arrayAmount[1] + '"}'
                part2Fix = '.' + arrayAmount[1] + "}"
                bdA = bdA.replace(part1, part1Fix).replace(part2, part2Fix)

            hshLb = hashlib.sha256
            strScK = str(secretKeyLoadedConfig)
            ln = 'latin-1'
            byteSck = bytes(strScK, ln)
            byteBody = bytes(bodyAux["req"], ln)
            sgnHashed = hmac.new(byteSck, msg=byteBody, digestmod=hshLb)
            sgnHashedHex = sgnHashed.hexdigest()

            if str(signatureReceived) == str(sgnHashedHex):
                bodyOk = {
                            "code": "100",
                            "message": "Solicitud con datos válidos"
                }
                statusOk = status.HTTP_200_OK
                return JsonResponse(bodyOk, status=statusOk, safe=False)
            else:
                bodyFail = {
                            "code": "111",
                            "message": "Solicitud con datos inválidos"
                }
                statusFail = status.HTTP_500_INTERNAL_SERVER_ERROR
                return JsonResponse(bodyFail, status=statusFail, safe=False)
