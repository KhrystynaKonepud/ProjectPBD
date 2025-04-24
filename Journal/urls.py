from django.urls import path
from Journal.views.auth_views import index, universal_login, logout_view
from Journal.views.admin_views import admin_dashboard
from Journal.views.lecturer_views import lecturer_dashboard
from Journal.views.student_views import student_dashboard

urlpatterns = [
    path('', index, name='home'),
    path('login/', universal_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('lecturer/dashboard/', lecturer_dashboard, name='lecturer_dashboard'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
]
