from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm

# Create your views here.
def signUp(request):
    form = UserCreationForm()
    return render(request, 'sign_up.html',{
        'title': 'Registro',
        'form': form,
    })

def signIn(request):
    form = AuthenticationForm()
    return render(request, 'sign_in.html', {
        'title': 'Iniciar Sesión',
        'form': form,
    })

def reset(request):
    form = PasswordResetForm()
    return render(request, 'reset.html', {
        'title': 'Iniciar Sesión',
        'form': form,
    })