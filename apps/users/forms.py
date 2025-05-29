from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    cedula_ti = forms.RegexField(
        regex=r'^\d+$',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Número de cédula o TI'})
        )
    
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
        )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
        )
    
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}),
        )
    
    nombres = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombres'}),
        )
    
    apellidos = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}),
        )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),
    )

    class Meta:
        model = User
        fields = ('cedula_ti', 'email', 'telefono', 'nombres', 'apellidos', 'fecha_nacimiento', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserAuthForm(forms.Form):
    cedula_ti = forms.RegexField(
        regex=r'^\d+$',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Número de cédula o TI'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
    )
