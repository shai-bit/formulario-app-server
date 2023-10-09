from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def submit_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("¡Login exitoso!")
        else:
            return HttpResponse("Nombre de usuario o contraseña incorrecta")
    else:
        return HttpResponse("Método no permitido", status=405)
