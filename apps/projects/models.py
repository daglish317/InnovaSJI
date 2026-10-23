import os

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify

def presentation_upload_path(instance, filename):

    extension = os.path.splitext(filename)[1].lower()
    nom = slugify(instance.title)[:60] or "projet"
    return f"presentations/{nom}{extension}"

class Level(models.TextChoices):
    L1 = 'L1', 'Licence 1'
    L2 = 'L2', 'Licence 2'
    L3 = 'L3', 'Licence 3'

class Status(models.TextChoices):
    EN_ATTENTE = 'EN_ATTENTE', 'En attente'
    VALIDE = 'VALIDE', 'Validé',
    REFUSE = 'REFUSE', 'Refusé'


class Project(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    problematic = models.TextField()
    solution = models.TextField()
    category = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.EN_ATTENTE
    )

    presentation_file = models.FileField(
        upload_to=presentation_upload_path,
        validators=[
        FileExtensionValidator(['mp4', 'mov', 'pptx','ppt', 'pdf']),
    ])
    presentation_web = models.FileField(upload_to="presentations/web/", blank=True, editable=False)

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                related_name='student'
    )
    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='members'
    )
    registration_number = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    level = models.CharField(max_length=2, choices=Level.choices, default=Level.L1)

    @property
    def is_chief(self):
        return self.user_id is not None

    def __str__(self):
        return self.name
