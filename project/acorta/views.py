from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import Url


# Create your views here.


@csrf_exempt
def process(request,recurso):
    metodo = request.method
    cuerpo = request.body

    lista_urls = Url.objects.all()

    if metodo == "POST":
        cuerpo = cuerpo.split("=",1)[1]
        print "cuerpo vale "+cuerpo

        if not cuerpo.startswith("http://"):
            cuerpo = "http://" + cuerpo
        try:
            elemento = Url.objects.get(url = cuerpo)
            respuesta = "<body>" +str(elemento.num)+ "=" +elemento.url+ "...ya estaba guardada!</body>"

        except Url.DoesNotExist:

            numero = len(lista_urls) + 1
            elem_aux = Url(num=numero, url=cuerpo)
            elem_aux.save()
            respuesta = "<body>" +str(numero)+ "=" +cuerpo+ "...direccion asignada con exito!</body>"


    elif metodo == "GET":

        if not recurso:
            respuesta = """
            <form action="" method="POST">
            <body>
                <input type="text" name="url" value="">
                </br>
                <input type="submit" value="Enviar">
            </body>
            </form>
            """

            respuesta+="<ul>"
            for elemento in lista_urls:
                respuesta += "<li>" +elemento.url+ ": " +str(elemento.num)+ "</li>"
            respuesta+="</ul>"

        elif recurso.isdigit():

            try:
                print "recurso = " + recurso

                elemento = Url.objects.get(num = int(recurso))

                respuesta = "<html><body><meta http-equiv='refresh'content='1 url="
                respuesta += elemento.url + "'></p></body></html>"

            except Url.DoesNotExist:

                respuesta = "<body>NO EXISTE</body>"


        else:
            respuesta = "<body>...URL NO VALIDA</body>"

    return HttpResponse(respuesta)
