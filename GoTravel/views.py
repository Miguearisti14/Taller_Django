from django.shortcuts import render, redirect
from .models import Destinos
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'index.html')

def formulario(request):
    return render(request, 'formulario.html')

# Mostrar los destinos
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

# Crear destinos
@login_required
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

# Eliminar destinos
@login_required
@require_http_methods(["DELETE"])
def delete_dest(request, destino_id):
    try:
        destino = Destinos.objects.get(id=destino_id)
        destino.delete()
        return JsonResponse({'status': 'success', 'message': 'Libro eliminado exitosamente'})
    except Destinos.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'El libro no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al eliminar el libro: {str(e)}'}, status=500)

# Editar destinos
@login_required
def edit_dest(request, destino_id):
    destino = Destinos.objects.get(id=destino_id)

    if request.method == 'POST':
        destino.destino = request.POST.get('destino')
        destino.pais = request.POST.get('pais')
        destino.continente = request.POST.get('continente')
        destino.idioma = request.POST.get('idioma')
        destino.moneda = request.POST.get('moneda')
        destino.save()
        messages.success(request, 'Destino actualizado correctamente.')
        return redirect('/destinos/')

    if request.method == 'GET':
        return render(request, 'editar.html', {'destino': destino})

# Registrar nuevo usuario
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

# Iniciar sesión
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

# Cerrar sesión
def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('/')