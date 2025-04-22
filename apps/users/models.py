from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class CustomUser(AbstractBaseUser):
    cedula_ti= models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=128, unique=True)

    USERNAME_FIELD = 'cedula_ti'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'telefono']

    def __str__(self):
        return self.cedula_ti