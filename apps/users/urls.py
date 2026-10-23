from django.urls import path
from .views import add_member_view, create_account, login_view, logout_view, members_admin_view

urlpatterns = [
    path('add-member/', add_member_view, name='add_member'),
    path('register/', create_account, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('gestion/candidates/', members_admin_view, name='students_list'),
]