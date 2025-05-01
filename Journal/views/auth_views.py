from django.shortcuts import render, redirect
from Journal.forms.login_form import UniversalLoginForm
from Journal.models.admin import Admin
from Journal.models.lecturer import Lecturer
from Journal.models.students import Students
from django.contrib.auth.hashers import check_password


def index(request):
    return render(request, 'index.html')


def universal_login(request):
    error = None

    if request.method == 'POST':
        form = UniversalLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Перевіряємо адміністратора
            admin = Admin.objects(email=email).first()
            if admin and check_password(password, admin.password):
                request.session['user_id'] = str(admin.id)
                request.session['role'] = 'admin'
                return redirect('admin_dashboard')

            # Перевіряємо викладача
            lecturer = Lecturer.objects(email=email).first()
            if lecturer and check_password(password, lecturer.password):
                request.session['user_id'] = str(lecturer.id)
                request.session['role'] = 'lecturer'
                return redirect('lecturer_dashboard')

            # Перевіряємо студента
            student = Students.objects(email=email).first()
            if student and check_password(password, student.password):
                request.session['user_id'] = str(student.id)
                request.session['role'] = 'student'
                return redirect('student_dashboard')

            error = "Користувача не знайдено або неправильний пароль."
    else:
        form = UniversalLoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})


def logout_view(request):
    request.session.flush()
    return redirect('login')
