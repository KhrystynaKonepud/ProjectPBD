from django.urls import path
from Journal.views.admin_views import (
    admin_dashboard,
    admin_users,
    admin_groups,
    admin_journal,
    admin_subjects,
    admin_profile,
    edit_admin_profile,
    admin_group_detail,
    user_detail,
    add_user,
    admin_add_group,
    admin_subject_detail,
    admin_delete_subject,
    admin_add_subject,
    admin_view_journal
)
from Journal.views.lecturer_views import lecturer_dashboard
from Journal.views.lecturer_views import create_journal
from Journal.views.lecturer_views import view_journal
from Journal.views.lecturer_views import delete_journal
from Journal.views.student_views import student_dashboard
from Journal.views.auth_views import index, universal_login, logout_view
from Journal.views.journal_detail_view import journal_detail

urlpatterns = [
    path('', index, name='index'),
    path('login/', universal_login, name='login'),
    path('logout/', logout_view, name='logout'),



    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', admin_users, name='admin_users'),
    path('admin/groups/', admin_groups, name='admin_groups'),
 #   path('admin/journals/', admin_journals, name='manage_journals'),


    path('admin/subjects/', admin_subjects, name='admin_subjects'),
    path('admin/subjects/add/', admin_add_subject, name='add_subject'),
    path('admin/subjects/<str:subject_id>/', admin_subject_detail, name='subject_detail'),
    path('admin/subjects/<str:subject_id>/delete/', admin_delete_subject, name='delete_subject'),


    path('admin/profile/', admin_profile, name='admin_profile'),
    path('admin/edit/', edit_admin_profile, name='edit_admin_profile'),

    path('admin/groups/add/', admin_add_group, name='add_group'),

    path('admin/groups/<str:group_id>/', admin_group_detail, name='group_detail'),

    path('admin/journals/', admin_journal, name='admin_journal'),
    path('admin/journal/<str:journal_id>/', admin_view_journal, name='admin_view_journal'),


    path('admin/user/<str:email>/', user_detail, name='user_detail'),
    path('admin/users/add/', add_user, name='add_user'),  # 🔧 Це маршрут на додавання
    path('lecturer/dashboard/', lecturer_dashboard, name='lecturer_dashboard'),
    path('lecturer/create_journal/', create_journal, name='create_journal'),
    path('lecturer/journal/<str:journal_id>/', view_journal, name='view_journal'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('lecturer/journal/<str:journal_id>/delete/', delete_journal, name='delete_journal'),
    path('student/journal/<str:journal_id>/', journal_detail, name='journal_detail'),
]
