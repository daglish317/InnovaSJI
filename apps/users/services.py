from apps.projects.models import Project
from django.core.exceptions import ValidationError
from django.db import transaction
from apps.projects.services.services import MAX_MEMBERS

@transaction.atomic
def add_member(form,chief):

    if not chief.project.id:
        raise ValidationError(f"Vous n'avez pas de projet. Créez un projet avant de continuer")

    project = Project.objects.select_for_update().get(id=chief.project.id)

    if project.members.count() >= MAX_MEMBERS:
        raise ValidationError(f"Vous avez déjà {MAX_MEMBERS} membres dans votre projet")

    member = form.save(commit=False)
    member.project = project
    member.save()

    return member