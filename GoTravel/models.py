from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuarios(models.Model):
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)

    class Meta:
        db_table = "usuarios"

class Destinos(models.Model):
    destino = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    continente = models.CharField(max_length=50)
    idioma = models.CharField(max_length=100)
    moneda = models.CharField(max_length=100)
    imagen = models.ImageField(
        upload_to='destinos/',    # Carpeta dentro de MEDIA_ROOT
        null=True,
        blank=True
    )

    class Meta:
        db_table = "Destinos"

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Comentarios"
        ordering = ['-fecha']