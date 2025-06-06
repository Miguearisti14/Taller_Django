from django.shortcuts import render, redirect, get_object_or_404
from .models import Destinos, Comentario
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import os


def index(request):
    return render(request, 'index.html')

def formulario(request):
    return render(request, 'formulario.html')

# Editar el perfil
@login_required
def editar_perfil(request):

    user = request.user

    if request.method == 'POST':
        try:
            # Actualizar campos
            user.first_name = request.POST.get('first_name').strip()
            user.last_name = request.POST.get('last_name').strip()

            # Guardar
            user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('/')
        
        except ValidationError as e:
            messages.error(request, f"Error: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error al actualizar el perfil: {str(e)}")

    return render(request, 'perfil.html', {'user': user})

# Mostrar los destinos
def destinos(request):
    # Parámetros de búsqueda y filtro
    query = request.GET.get('q', '').strip()
    pais_filtro = request.GET.get('pais', '').strip()
    continente_filtro = request.GET.get('continente', '').strip()
    idioma_filtro = request.GET.get('idioma', '').strip()

    # Partimos de todos los destinos
    destinos_list = Destinos.objects.all()

    # Aplicamos búsqueda por nombre
    if query:
        destinos_list = destinos_list.filter(destino__icontains=query)

    # Aplicamos filtros si están definidos
    if pais_filtro:
        destinos_list = destinos_list.filter(pais=pais_filtro)
    if continente_filtro:
        destinos_list = destinos_list.filter(continente=continente_filtro)
    if idioma_filtro:
        destinos_list = destinos_list.filter(idioma=idioma_filtro)

    # Paginación (8 por página)
    paginator = Paginator(destinos_list, 8)
    page_number = request.GET.get('page')
    destinos_page = paginator.get_page(page_number)

    # Generamos las listas únicas para los selects
    paises = Destinos.objects.values_list('pais', flat=True).distinct().order_by('pais')
    continentes = Destinos.objects.values_list('continente', flat=True).distinct().order_by('continente')
    idiomas = Destinos.objects.values_list('idioma', flat=True).distinct().order_by('idioma')

    return render(request, 'destinos.html', {
        'destinos': destinos_page,
        'query': query,
        'paises': paises,
        'continentes': continentes,
        'idiomas': idiomas,
        'pais_filtro': pais_filtro,
        'continente_filtro': continente_filtro,
        'idioma_filtro': idioma_filtro,
    })

# Sección de comentarios
def experiencias(request):
    if request.method == 'POST':
        if not request.user.has_perm('GoTravel.add_comentarios'):
            return render(request,"error.html")
        mensaje = request.POST.get('mensaje', '').strip()
        if mensaje:
            Comentario.objects.create(usuario=request.user, mensaje=mensaje)
            return redirect('/experiencias')

    comentarios = Comentario.objects.all()
    return render(request, 'experiencias.html', {'comentarios': comentarios})

# Crear destinos
def create_dest(request):
    if not request.user.has_perm('GoTravel.add_destinos'):
        return render(request,"error.html")
    if request.method == 'GET':
        return render(request, 'agregar.html')

    if request.method == 'POST':
        print(f"POST recibido para crear nuevo destino")  # Depuración 1
        try:
            # Obtener y limpiar datos del formulario
            destino = request.POST.get('destino').strip()
            pais = request.POST.get('pais').strip()
            continente = request.POST.get('continente').strip()
            idioma = request.POST.get('idioma').strip()
            moneda = request.POST.get('moneda').strip()

            imagen = request.FILES.get('imagen')
            if imagen:
                content_type = imagen.content_type
                if not content_type.startswith('image/'):
                    raise ValidationError("El archivo subido no es una imagen válida.")

                ext = os.path.splitext(imagen.name)[1].lower()
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.heic', '.heif'}
                if ext not in allowed_extensions:
                    raise ValidationError(f"Extensión no permitida: {ext}. Usa: {', '.join(allowed_extensions)}")

                # Generar nombre de archivo seguro
                filename = f"{destino.lower().replace(' ', '_')}{ext}"
                imagen = imagen 
            else:
                imagen = None 

            # Crear el nuevo destino
            destinos = Destinos(
                destino=destino,
                pais=pais,
                continente=continente,
                idioma=idioma,
                moneda=moneda,
                imagen=imagen
            )
            destinos.save()

            messages.success(request, 'Destino agregado exitosamente')
            return redirect('/destinos/')

        except ValidationError as e:
            messages.error(request, f"Error: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error al crear el destino: {str(e)}")

    return HttpResponse("Método no permitido", status=405)

# Eliminar destinos
@login_required
@require_http_methods(["DELETE"])
def delete_dest(request, destino_id):
    if not request.user.has_perm('GoTravel.delete_destinos'):
        return render(request,"error.html")
    try:
        destino = Destinos.objects.get(id=destino_id)
        destino.delete()
        return JsonResponse({'status': 'success', 'message': 'Destino eliminado exitosamente'})
    except Destinos.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'El destino no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al eliminar el destino: {str(e)}'}, status=500)

# Editar destinos
@login_required
def edit_dest(request, destino_id):
    if not request.user.has_perm('GoTravel.change_destinos'):
        return render(request,"error.html")
    destino = get_object_or_404(Destinos, id=destino_id)

    if request.method == 'POST':
        try:
            # Actualizar campos de texto
            destino.destino = request.POST.get('destino').strip()
            destino.pais = request.POST.get('pais').strip()
            destino.continente = request.POST.get('continente').strip()
            destino.idioma = request.POST.get('idioma').strip()
            destino.moneda = request.POST.get('moneda').strip()

            # Manejar la imagen
            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                # Validar que el archivo es una imagen
                content_type = imagen.content_type
                if not content_type.startswith('image/'):
                    raise ValidationError("El archivo subido no es una imagen válida.")

                # Validar la extensión del archivo
                ext = os.path.splitext(imagen.name)[1].lower()
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.heic', '.heif'}
                if ext not in allowed_extensions:
                    raise ValidationError(f"Extensión no permitida: {ext}. Usa: {', '.join(allowed_extensions)}")

                # Generar un nombre de archivo seguro
                filename = f"{destino.destino.lower().replace(' ', '_')}{ext}"
                destino.imagen.delete(save=False)  # Eliminar la imagen anterior, si existe
                destino.imagen.save(filename, imagen, save=True)
                print(f"Imagen guardada en: {destino.imagen.path}")  # Agrega esta línea para depuración

            # Guardar los cambios
            destino.save()
            messages.success(request, 'Destino actualizado correctamente.')
            return redirect('/destinos/')

        except ValidationError as e:
            messages.error(request, f"Error: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error al actualizar el destino: {str(e)}")

    return render(request, 'editar.html', {'destino': destino})

# Registrar nuevo usuario
def registrar_usuario(request):
    grupos = Group.objects.all()

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'mostrar_signin': True,
            'groups': grupos
        })

    # POST
    username   = request.POST.get('username', '').strip()
    password   = request.POST.get('password', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name  = request.POST.get('last_name', '').strip()
    group_id   = request.POST.get('group')

    # Validaciones básicas
    if not (first_name and last_name and username and password and group_id):
        messages.error(request, 'Todos los campos son obligatorios.')
        return render(request, 'signin.html', {
            'mostrar_signin': True,
            'groups': grupos,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'selected_group': group_id
        })

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Ese usuario ya existe.')
        return render(request, 'signin.html', {
            'mostrar_signin': True,
            'groups': grupos,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'selected_group': group_id
        })

    # Crear usuario
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=username
    )

    # Asignar el rol seleccionado
    try:
        grupo = Group.objects.get(id=group_id)
        user.groups.add(grupo)
    except Group.DoesNotExist:
        pass

    messages.success(request, 'Usuario registrado correctamente.')
    return redirect('/login')

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