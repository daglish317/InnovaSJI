from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = UsernameField(label="Matricule")

    def clean_username(self):
        writed = self.cleaned_data['username'].strip()
        uppercased = writed.upper()
        return uppercased if User.objects.filter(username=uppercased).exists() else writed