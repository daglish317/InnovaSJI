from django.core.exceptions import ValidationError
from apps.projects.models import Student, Project
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

SIZE_MAX_MO = 100
MAX_MEMBERS = 5

def validate_size(file):
    if file.size > SIZE_MAX_MO * 1024 * 1024:
        raise ValidationError(f"Le fichier ne doit pas exéder {SIZE_MAX_MO} Mo")

@transaction.atomic
def create_project(chief_form,project_form):
    d = chief_form.cleaned_data
    user = User.objects.create_user(username=d['registration_number'],
                                    password=d['password1'],
                                    first_name=d['firstname'],
                                    last_name=d['name'],
                                    email=d['email']
                                    )
    project = project_form.save()
    chief = chief_form.save(commit=False)
    chief.user = user
    chief.project = project
    chief.save()
    return chief
