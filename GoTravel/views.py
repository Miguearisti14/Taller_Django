from django.shortcuts import render

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