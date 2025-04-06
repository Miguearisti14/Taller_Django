from django.db import models

# Create your models here.
class Usuarios(models.Model):
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)

    class Meta:
        db_table = "usuarios"