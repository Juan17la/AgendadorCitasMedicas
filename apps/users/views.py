from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserAuthForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def signUp_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('paciente_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def signIn_view(request):
    if request.method == 'POST':
        form = UserAuthForm(request.POST)
        if form.is_valid():
            cedula_ti = form.cleaned_data['cedula_ti']
            password = form.cleaned_data['password']
            user = authenticate(request, username=cedula_ti, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirige según el rol del usuario
                    if user.rol == 'Doctor':
                        return redirect('paciente_dashboard')
                    elif user.rol == 'Administrador':
                        return redirect('adminDashboard')
                    else:
                        return redirect('paciente_dashboard')
                else:
                    form.add_error(None, 'Tu cuenta está desactivada.')
            else:
                form.add_error(None, 'Cédula o contraseña inválidos')
    else:
        form = UserAuthForm()
    
    return render(request, 'signin.html', {
        'form': form,
    })

def signOut_view(request):
    logout(request)
    return redirect('index')
