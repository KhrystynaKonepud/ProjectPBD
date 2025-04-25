from django.shortcuts import render, redirect, get_object_or_404
from mongoengine.errors import NotUniqueError
from Journal.models.admin import Admin
from Journal.forms.profile_edit_form import AdminProfileForm
from django.contrib.auth.hashers import make_password
from Journal.models.students import Students
from Journal.models.lecturer import Lecturer
from Journal.models.students import Students as Student
from Journal.models.lecturer import Lecturer
from Journal.models.admin import Admin
from Journal.models.groups import Groups
from django.contrib import messages




def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def admin_users(request):
    return render(request, 'admin_panel/users.html')

def admin_groups(request):
    return render(request, 'admin_groups.html')

def admin_journals(request):
    return render(request, 'admin_journals.html')

def admin_subjects(request):
    return render(request, 'admin_subjects.html')

def admin_profile(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    try:
        admin = Admin.objects.get(id=request.session.get('user_id'))
    except Admin.DoesNotExist:
        return redirect('login')

    context = {
        'name': admin.name,
        'email': admin.email,
        'masked_password': '****',
    }

    return render(request, 'admin_panel/profile.html', context)

def edit_admin_profile(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    try:
        admin = Admin.objects.get(id=request.session.get('user_id'))
    except Admin.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        form = AdminProfileForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['name']:
                admin.name = form.cleaned_data['name']
            if form.cleaned_data['email']:
                admin.email = form.cleaned_data['email']
            if form.cleaned_data['password']:
                admin.password = make_password(form.cleaned_data['password'])  # ХЕШУЄМО!
            admin.save()
            return redirect('admin_profile')
    else:
        form = AdminProfileForm(initial={
            'name': admin.name,
            'email': admin.email
        })

    return render(request, 'admin_panel/edit_profile.html', {'form': form})

def admin_users(request):
    students = Students.objects.all()
    lecturers = Lecturer.objects.all()
    admins = Admin.objects.all()

    return render(request, 'admin_panel/users.html', {
        'students': students,
        'lecturers': lecturers,
        'admins': admins,
    })

def user_detail(request, email):
    user = (
        Student.objects(email=email).first()
        or Lecturer.objects(email=email).first()
        or Admin.objects(email=email).first()
    )
    if not user:
        return render(request, "404.html", status=404)

    return render(request, "admin_panel/user_detail.html", {"user": user})



def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Хешування пароля
        hashed_password = make_password(password)

        # Пробуємо отримати group_id з форми (може бути порожнім)
        group_id = request.POST.get('group_id')
        group = None
        if group_id:
            try:
                group = Groups.objects.get(id=group_id)
            except Groups.DoesNotExist:
                group = None

        # Створення користувача
        if role == 'student':
            student = Students(name=name, email=email, password=hashed_password)
            if group:
                student.group = group
            student.save()
        elif role == 'lecturer':
            Lecturers(name=name, email=email, password=hashed_password).save()
        elif role == 'admin':
            Admin(name=name, email=email, password=hashed_password).save()

        messages.success(request, 'Користувача успішно додано.')
        return redirect('admin_users')

    groups = Groups.objects()
    return render(request, 'admin_panel/add_user.html', {'groups': groups})
