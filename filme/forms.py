from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


class CriarContaForms(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')