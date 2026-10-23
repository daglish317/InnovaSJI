from django.urls import path
from .views import create_project_view, project_detail_view, project_list_admin_view, project_detail_admin_view, validate_reject_project_view

urlpatterns = [
    path('create-project', create_project_view, name='create-project'),
    path('project-detail/<int:pk>', project_detail_view, name='my_project'),
    path('gestion/project-list', project_list_admin_view, name='project_list'),
    path('gestion/project-detail/<int:pk>', project_detail_admin_view, name='project_detail_admin'),
    path('gestion/action/<int:pk>', validate_reject_project_view, name='validate_or_reject'),
]