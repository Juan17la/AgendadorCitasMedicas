from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Se creo un usuario personalizado usando AbstractBaseUser

class CustomUserManager(UserManager):
    def _create_user(self, cedula_ti, email, password, **extra_fields):
        if not cedula_ti:
            raise ValueError('No se ha puesto ninguna cédula o documento de identidad')
        
        if not email:
            raise ValueError('No se ha puesto ningún email')

        email = self.normalize_email(email)
        user = self.model(cedula_ti=cedula_ti, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, cedula_ti=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(cedula_ti, email, password, **extra_fields)

    def create_superuser(self, cedula_ti=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(cedula_ti, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Paciente', 'Paciente'),
        ('Doctor', 'Doctor'),
        ('Administrador', 'Administrador'),
    )

    cedula_ti = models.CharField(max_length=150, unique=True)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Paciente')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)   # 🚨 <-- AGREGA ESTA LÍNEA
    email_verificado = models.BooleanField(default=False)

    fecha_registro = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'cedula_ti'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'fecha_nacimiento', 'telefono', 'email']

    def __str__(self):
        return self.cedula_ti

    