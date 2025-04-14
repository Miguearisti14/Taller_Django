"""
URL configuration for PythonServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import GoTravel.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GoTravel.views.index),
    path('formulario/', GoTravel.views.formulario),
    path('login/', GoTravel.views.iniciar_sesion),
    path('signin/', GoTravel.views.registrar_usuario),
    path('destinos/', GoTravel.views.destinos),
    path('agregar/', GoTravel.views.create_dest),
    path('delete_dest/<int:destino_id>/', GoTravel.views.delete_dest),
    path('logout/', GoTravel.views.cerrar_sesion),
    path('edit_dest/<int:destino_id>/', GoTravel.views.edit_dest)
]
