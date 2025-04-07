from django.shortcuts import render, redirect
from .models import Destinos
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



# Create your views here.
def index(request):
    return render(request, 'index.html')

def formulario(request):
    return render(request, 'formulario.html')



def destinos(request):
    query = request.GET.get('q', '')
    if query:
        destinos_list = Destinos.objects.filter(destino__icontains=query)
    else:
        destinos_list = Destinos.objects.all()

    paginator = Paginator(destinos_list, 9)
    page_number = request.GET.get('page')
    destinos = paginator.get_page(page_number)

    return render(request, 'destinos.html', {'destinos': destinos, 'query': query})

def create_dest(request):
    if request.method == 'GET':
        return render(request, 'agregar.html')

    if request.method == 'POST':
        destino = request.POST.get('destino')
        pais = request.POST.get('pais')
        continente = request.POST.get('continente')
        idioma = request.POST.get('idioma')
        moneda = request.POST.get('moneda')
        
        destinos = Destinos(
            destino=destino,
            pais=pais,
            continente=continente,
            idioma=idioma,
            moneda=moneda
        )
        destinos.save()
    
        messages.success(request, 'Destino agregado exitosamente')
        return redirect('/destinos/')
    
    return HttpResponse("Metodo no permitido",status=405)

def registrar_usuario(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'mostrar_signin': True
    })

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese usuario ya existe.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('/login/')
        

    return render(request, 'signin.html', {
        'mostrar_sigin': True
    })


def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
        'mostrar_signin': True
    })

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            
            return redirect('/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html', {
        'mostrar_signin': True
    })