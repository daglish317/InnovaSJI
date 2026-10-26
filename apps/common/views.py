from django.shortcuts import render, get_object_or_404
from apps.projects.models import Student

# Create your views here.
def home_page_view(request, page):
    templates = {
        "home": "public/home.html",
        "giveaway": "public/Giveaway.html",
        "rules": "public/rules.html",
        "calendar": "public/calendar.html",
        "sponsors": "public/sponsors.html",
        "contact": "public/contact.html",
    }
    template = templates.get(page)
    if template is None:
        raise Http404
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, template)
        else:
            project = get_object_or_404(Student, user=request.user).project
            context = {'project': project}
            return render(request, template, context)

    return render(request, template)