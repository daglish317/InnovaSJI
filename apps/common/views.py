from django.shortcuts import render, get_object_or_404
from apps.projects.models import Student

# Create your views here.
def home_page_view(request):

    project = get_object_or_404(Student, user=request.user).project
    context = {'project': project}
    return render(request, 'public/home.html', context)