from django.urls import path
from Journal.views.auth_views import index, universal_login, logout_view
from Journal.views.admin_views import (
    admin_dashboard,
    admin_users,
    admin_groups,
    admin_journals,
    admin_subjects,
    admin_profile,  # ← імпорт додано
    edit_admin_profile
)
from Journal.views.lecturer_views import lecturer_dashboard
from Journal.views.lecturer_views import create_journal
from Journal.views.student_views import student_dashboard

urlpatterns = [
    path('', index, name='index'),

    path('login/', universal_login, name='login'),
    path('logout/', logout_view, name='logout'),

    # Дашборд адміністратора + вкладки
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', admin_users, name='manage_users'),
    path('admin/groups/', admin_groups, name='manage_groups'),
    path('admin/journals/', admin_journals, name='manage_journals'),
    path('admin/subjects/', admin_subjects, name='manage_subjects'),
    path('admin/profile/', admin_profile, name='admin_profile'),  # ← новий маршрут
    path('admin/edit/', edit_admin_profile, name='edit_admin_profile'),


    # Дашборди викладача та студента
    path('lecturer/dashboard/', lecturer_dashboard, name='lecturer_dashboard'),
    path('lecturer/create_journal/', create_journal, name='create_journal'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
]
