"""Filtres de template du front Innova.

À placer dans le dossier `templatetags/` d'une de vos applications
(ex. `core/templatetags/innova_ui.py`, avec un `__init__.py`), puis
`{% load innova_ui %}` dans les templates.
"""
import os

from django import forms, template

register = template.Library()


@register.filter
def bs(field, extra=""):
    """Rend un champ de formulaire avec les classes Bootstrap adaptées.

    - ajoute form-control / form-select / form-check-input selon le widget
    - ajoute is-invalid + aria-invalid quand le champ a des erreurs
    - relie le champ à son message d'erreur (aria-describedby)
    """
    widget = field.field.widget
    input_type = getattr(widget, "input_type", "")
    if isinstance(widget, (forms.Select, forms.SelectMultiple)):
        base = "form-select"
    elif input_type == "checkbox":
        base = "form-check-input"
    else:
        base = "form-control"

    classes = [widget.attrs.get("class", ""), base, extra]
    if field.errors:
        classes.append("is-invalid")
    attrs = {"class": " ".join(c for c in classes if c)}
    if field.errors:
        attrs["aria-invalid"] = "true"
        attrs["aria-describedby"] = f"{field.auto_id}_err"
    if isinstance(widget, forms.Textarea) and widget.attrs.get("rows") in (None, "10"):
        attrs["rows"] = "4"
    return field.as_widget(attrs=attrs)


@register.filter
def basename(value):
    """Nom de fichier seul d'un FileField (sans le chemin d'upload)."""
    name = getattr(value, "name", value) or ""
    return os.path.basename(str(name))


VIDEO_EXT = {"mp4", "mov", "m4v", "webm"}
DOC_LABELS = {"pptx": "PowerPoint", "ppt": "PowerPoint", "pdf": "PDF"}


@register.filter
def file_ext(value):
    """Extension en minuscules, sans le point : 'pptx', 'mp4'..."""
    name = getattr(value, "name", value) or ""
    return os.path.splitext(str(name))[1].lstrip(".").lower()


@register.filter
def file_kind(value):
    """'video' si le fichier est une vidéo, sinon 'document'."""
    return "video" if file_ext(value) in VIDEO_EXT else "document"


@register.filter
def file_label(value):
    """Libellé lisible du format : PowerPoint, PDF, ou l'extension en majuscules."""
    ext = file_ext(value)
    return DOC_LABELS.get(ext, ext.upper() or "Fichier")


@register.filter
def file_size(value):
    """Taille lisible (ex. '4,2 Mo'). Renvoie '' si le fichier est introuvable."""
    from django.template.defaultfilters import filesizeformat
    try:
        return filesizeformat(value.size)
    except (OSError, ValueError, AttributeError):
        return ""