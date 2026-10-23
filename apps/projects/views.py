from django.shortcuts import render, get_object_or_404, redirect
from .form import ProjectForm
from apps.projects.services.services import create_project, validate_size
from django.contrib.auth.decorators import login_required
from .models import Student, Project
from apps.projects.services.services import MAX_MEMBERS
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import Http404

# rappel pour Assir: A utiliser
def create_project_view(request):
    student = get_object_or_404(Student, user=request.user)

    if student.project:
        return render(request,'404.html')

    form = ProjectForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        try:
            validate_size(request.FILES)
            create_project(student,form)

        except ValidationError as e:
            form.add_error(None, e)
        else:
            return render(request,'error.html',{'form':form})

    return render(request,'espace/create_project.html',{'form':form})

@login_required
def project_detail_view(request, pk):

    student = request.user.student
    if not student.project.id == pk:
        raise Http404

    project = get_object_or_404(Project, id=pk)
    students = Student.objects.filter(project=project)
    context = {
        'project': project,
        'students': students,
        'max_members': MAX_MEMBERS,
    }
    return render(request, 'espace/my_project.html',context)


@login_required
def project_list_admin_view(request):

    if request.user.is_staff:


        projects = Project.objects.prefetch_related('members').all()

        context = {
            'projects': projects,
            'max_members': MAX_MEMBERS,
        }

        return render(request, 'gestion/projects.html',context)

    return render(request, '404.html')


@login_required
def project_detail_admin_view(request, pk):
    if not request.user.is_staff:
        return render(request, '404.html')

    project = get_object_or_404(Project, id=pk)
    students = Student.objects.filter(project=project)
    context = {
        'project': project,
        'students': students,
    }
    return render(request, 'gestion/project_detail.html',context)

@login_required
@require_POST
def validate_reject_project_view(request, pk):
    if not request.user.is_staff:
        raise Http404

    project = get_object_or_404(Project, id=pk)
    action = request.POST.get("action")
    source = request.POST.get("source")


    if action == "accept":
        project.status = "VALIDE"
        project.save()
        messages.success(request, f"Le projet « {project.title} » a été validé.")
    elif action == "reject":
        project.status = "REFUSE"
        project.save()
        messages.success(request, f"Le projet « {project.title} » a été refusé.")
    else:
        messages.error(request, "Action non reconnue.")

    if source == "detail":
        return redirect("project_detail_admin", pk=pk)
    return redirect("project_list")