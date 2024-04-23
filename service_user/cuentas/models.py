# En models.py
from django.db import models

class Usuario(models.Model):
    cedula = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=10)
    password  = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre