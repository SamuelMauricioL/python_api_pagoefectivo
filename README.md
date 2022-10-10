# Título del Proyecto

Pago Efectivo

## Comenzando 🚀

_Proyecto desarrollado en python + django, para la generación de CIP_

### Pre-requisitos 📋

```
	- python 3.7 (verificar variables de entorno)
```

```
	- pip (gestor de paquetes para instalar dependencias posteriormente)
```

## Instalación 🔧

_Ubicarse en la raiz del proyecto, a la altura del archivo "manage.py" y ejecutar los siguientes comandos en el terminal:_

```
	- pip install appname
```

```
	- pip install djangorestframework
```

```
	- pip install hashlib
```

```
	- pip install hmac
```

```
	- pip install requests
```

```
	- pip install beautifulsoup4
```

## Run server

_Ejecutar los siguientes en el terminal_

```
	- python manage.py makemigrations
```

```
	- python manage.py migrate
```

```
	- python manage.py runserver
```
## Visualización

_El proyecto va abrir en la siguiente ruta "http://127.0.0.1:8000/", copiar y pegar en el navegador._

## API (@api_view(["GET", "POST"]), "http://127.0.0.1:8000/validation")

_Este API de tipo POST, se puede utilizar desde POSTMAN con las siguiente credenciales._

```
1 HEADER:
```
```
1.2 { 
key: "PE-Signature",
value: {{signature}}
}
```

```
2 BODY
```

```
2.1 { 
"eventType":"cip.paid",
"operationNumber":{{}},
"data":{
	"cip":{{}},
	"currency":{{}}",
	"amount":{{}}
	}
}
```

```
3 RESPONSE
```

```
3.1 STATUS OK
response: {
"code": "100",
"message": "Solicitud con datos válidos"
}
status: 200
```

```
3.2 STATUS 500_INTERNAL_SERVER_ERROR
response: {
"code": "111",
"message": "Solicitud con datos inválidos"
}
		
html: "weather/empty.html"
status: 500
```