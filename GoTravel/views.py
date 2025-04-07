from django.shortcuts import render
from .models import Destinos
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, 'index.html')

def formulario(request):
    return render(request, 'formulario.html')

def login(request):
    return render(request, 'login.html', {
        'mostrar_sigin': True
    })

def signin(request):
    return render(request, 'signin.html', {
        'mostrar_sigin': True
    })

def destinos(request):
    query = request.GET.get('q', '')
    if query:
        destinos_list = Destinos.objects.filter(destino__icontains=query)
    else:
        destinos_list = Destinos.objects.all()

    paginator = Paginator(destinos_list, 9)  # 9 destinos por página
    page_number = request.GET.get('page')
    destinos = paginator.get_page(page_number)

    return render(request, 'destinos.html', {'destinos': destinos, 'query': query})