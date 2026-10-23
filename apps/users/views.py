from django.shortcuts import render ,get_object_or_404,redirect, resolve_url
from .services import add_member
from apps.projects.models import Student, Project
from apps.projects.form import MemberForm, InscriptionForm, ProjectForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from apps.projects.services.services import MAX_MEMBERS, create_project
from .forms import LoginForm
from django.http import Http404

@login_required(login_url='/accounts/login/')
def add_member_view(request):

    chief = get_object_or_404(Student, user=request.user)
    project = get_object_or_404(Project, id=chief.project.id)
    remaining_candidates_count = Student.objects.filter(project=project).count()

    if (request.method == 'POST'):

        form = MemberForm(request.POST)

        if form.is_valid():
            try:
                member = add_member(form, chief)
                return redirect(f'/project-detail/{project.id}')
            except ValidationError as e:
                form.add_error(None,e)
        context = {
            "form": form,
            "project": project,
            "remaining_candidates_count": remaining_candidates_count,
            "MAX_MEMBERS": MAX_MEMBERS,
        }
        return render(request,'espace/add_member.html', context)

    form = MemberForm()
    context = {
        "form": form,
        "project": project,
        "remaining_candidates_count": remaining_candidates_count,
        "MAX_MEMBERS": MAX_MEMBERS,
    }

    return render(request,'espace/add_member.html', context)

def create_account(request):
    if request.user.is_authenticated:
        raise Http404

    if(request.method == 'POST'):
        chief_form = InscriptionForm(request.POST, prefix='chief')
        project_form = ProjectForm(request.POST, request.FILES, prefix='project')
        if chief_form.is_valid() and project_form.is_valid():
            chief = create_project(chief_form, project_form)
            login(request, chief.user)
            return redirect(f'/project-detail/{chief.project.id}')
        context ={
            "chief_form": chief_form,
            "project_form": project_form
        }
        return render(request,'espace/inscription.html', context)

    context = {
        "chief_form" : InscriptionForm(prefix='chief'),
        "project_form" : ProjectForm(prefix='project')
    }

    return render(request,'espace/inscription.html', context)


def redirect_to(user):
    if user.is_staff:
        return redirect('project_list')
    return redirect('my_project', pk=user.student.project_id)


def login_view(request):
    if request.user.is_authenticated:
        return redirect_to(request.user)

    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect_to(user)
    return render(request, 'public/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


@login_required
def members_admin_view(request):

    if not request.user.is_staff:
        raise Http404
    students = Student.objects.all().order_by('project_id')
    return render(request, 'gestion/students.html', {'students': students})