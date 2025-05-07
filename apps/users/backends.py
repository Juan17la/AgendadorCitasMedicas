from django.contrib.auth.backends import BaseBackend
from .models import User  # Asegúrate de que este import esté bien
from django.contrib.auth.hashers import check_password

class CedulaAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(cedula_ti=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
