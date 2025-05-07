from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserAuthForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.

def signUp_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')
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
                login(request, user)
                return redirect('index')  
            else:
                form.add_error(None, 'Cédula o contraseña inválidos')
    else:
        form = UserAuthForm()
    return render(request, 'signin.html', {'form': form})

def signOut_view(request):
    logout(request)
    return redirect('index')
