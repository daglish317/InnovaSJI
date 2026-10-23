import threading
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.projects.models import Project
from apps.projects.services.utils import (is_video, make_web_version, web_version_path)


@receiver(post_save, sender=Project)
def prepare_web_video(sender, instance, **kwargs):
    if not instance.presentation_file:
        return
    if not is_video(instance.presentation_file.name):
        return
    if instance.presentation_web.name == web_version_path(instance.presentation_file.name):
        return

    transaction.on_commit(
        lambda: threading.Thread(target=make_web_version, args=(instance.pk,), daemon=True).start()
    )