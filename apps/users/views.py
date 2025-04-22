from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from .forms import CustomUserCreationForm, CustomUserAuthForm
from .models import CustomUser
from django.contrib.auth import login, authenticate
from django.db import IntegrityError

# Create your views here.
def signUp(request):
    
    if request.method == 'GET':
        return render(request, 'sign_up.html',{
            'title': 'Registro',
            'form': CustomUserCreationForm(),
        })
        
    form = CustomUserCreationForm(request.POST)
    
    if form.is_valid():
        password = form.cleaned_data['password']
        password2 = form.cleaned_data['confirm_password']
         
        if password != password2:
            return render(request, 'sign_up.html',{
            'title': 'Registro',
            'form': form,
            'error': 'Las contraseñas no coinciden!'
            })
        try:
            newUser = CustomUser.objects.create(
                cedula_ti = form.cleaned_data['cedula_ti'],
                email = form.cleaned_data['email'],
                telefono = form.cleaned_data['telefono'],
                nombres = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
                fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],
                password = password
            )
            
            login(request, newUser)
            return redirect('dashboardPaciente')
        
        except IntegrityError:
            return render(request, 'sign_up.html',{
            'title': 'Registro',
            'form': form,
            'error':'El usuario ya existe!'
            })

    return render(request, 'sign_up.html',{
            'title': 'Registro',
            'form': form,
    })
        

def signIn(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html', {
            'title': 'Iniciar Sesión',
            'form': CustomUserAuthForm,
        })
        
    form = CustomUserAuthForm()
    if form.is_valid():
        cedula_ti = form.cleaned_data['cedula_ti']
        password = form.cleaned_data['password']
        
        user = authenticate(request, cedula_ti=cedula_ti, password=password)
        
        if user is None:
            return render(request, 'sign_in.html', {
            'title': 'Iniciar Sesión',
            'form': form,
            'error':'El usuario no existe!'
        })
            
        else:
            login(request, user)
            return redirect('dashboardPaciente')
    
    return render(request, 'sign_in.html', {
            'title': 'Iniciar Sesión',
            'form': form,
            'error':'El usuario no existe!'
        })
            
def reset(request):
    form = PasswordResetForm()
    return render(request, 'reset.html', {
        'title': 'Iniciar Sesión',
        'form': form,
    })