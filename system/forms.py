# usuarios/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario

class UsuarioCadastroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'genero', 'data_nascimento', 'time', 'password1', 'password2']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Usuário'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    )