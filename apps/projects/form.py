from django import forms
from .models import *
from django.db import transaction
from django.contrib.auth.password_validation import validate_password


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['registration_number','name','firstname', 'email', 'phone', 'level']
        error_messages = {
            "registration_number": {"unique": "Ce matricule est déjà inscrit dans un projet"},
            "email": {"unique":"Cet email est déjà utilisé"}
        }

        def clean_registration_number(self):
            return self.cleaned_data['registration_number'].strip().upper()

class MemberForm(StudentForm):
    pass

class InscriptionForm(StudentForm):

    password1 = forms.CharField(label="Mot de passe",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe",widget=forms.PasswordInput)

    def clean_password1(self):
        pwd = self.cleaned_data['password1']
        validate_password(pwd)
        return pwd

    def clean(self):
        data = super().clean()
        if data.get("password1") != data.get("password2"):
            self.add_error('password2', 'Le mot de passe ne correspond pas')
        return data



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','problematic','solution','category','presentation_file']
        widgets = {
            'description': forms.Textarea(attrs={'class': "full"}),
            'problematic': forms.Textarea(attrs={'class': "full"}),
            'solution': forms.Textarea(attrs={'class': "full"}),
        }