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
from Journal.models.subjects import Subjects
from mongoengine.errors import DoesNotExist
from bson import ObjectId
from bson.dbref import DBRef
from mongoengine.base import get_document
from mongoengine.queryset.visitor import Q
from Journal.models.journal import Journal
from mongoengine.errors import DoesNotExist
from django.http import Http404
from mongoengine.connection import get_db
from Journal.models.groups import Groups as Group





def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def admin_users(request):
    return render(request, 'admin_panel/users.html')






def admin_subjects(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        subject_id = request.POST.get('subject_id')

        if action == 'delete' and subject_id:
            try:
                subject = Subjects.objects.get(id=subject_id)
                subject.delete()
            except Subjects.DoesNotExist:
                pass  # можна додати повідомлення про помилку

        return redirect('admin_subjects')  # name у urls.py

    subjects = Subjects.objects.all()
    return render(request, 'admin_panel/subjects.html', {'subjects': subjects})


def admin_subject_detail(request, subject_id):
    subject = Subjects.objects(id=subject_id).first()

    if not subject:
        return render(request, '404.html', status=404)

    lecturer = subject.lecturer  # тут просто отримуємо викладача, БЕЗ fetch()

    context = {
        'subject': subject,
        'lecturer': lecturer
    }
    return render(request, 'admin_panel/subject_detail.html', context)

def admin_delete_subject(request, subject_id):
    subject = Subjects.objects(id=subject_id).first()

    if subject:
        # Перед видаленням — видалити цей предмет у всіх викладачів
        lecturers = subject.lecturer
        for lecturer in lecturers:
            if hasattr(lecturer, 'subjects') and lecturer.subjects:
                updated_subjects = [subj for subj in lecturer.subjects if subj.id != subject.id]
                lecturer.update(set__subjects=updated_subjects)  # ОНОВЛЮЄМО через update() щоб не видалявся список

        # Тепер видаляємо саму дисципліну
        subject.delete()

    return redirect('admin_subjects')






def admin_add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        lecturer_ids = request.POST.getlist('lecturers')  # важливо getlist()

        lecturer_refs = [Lecturer.objects.get(id=lect_id) for lect_id in lecturer_ids]

        new_subject = Subjects(
            name=name,
            description=description,
            lecturer=lecturer_refs  # тепер тут список викладачів
        )
        new_subject.save()

        # Додаємо цю дисципліну кожному викладачу
        for lecturer in lecturer_refs:
            if not hasattr(lecturer, 'subjects') or lecturer.subjects is None:
                lecturer.subjects = []
            lecturer.subjects.append(new_subject)
            lecturer.save()

        return redirect('admin_subjects')

    lecturers = Lecturer.objects.all()
    return render(request, 'admin_panel/add_subject.html', {'lecturers': lecturers})




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

def admin_groups(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = Groups.objects.get(id=group_id)

        # Очищаємо поле group у студентів
        for student in group.students:
            student.update(set__group=None)

        group.delete()
        return redirect('admin_groups')

    groups = Groups.objects.all()
    return render(request, 'admin_panel/groups.html', {'groups': groups})


def admin_group_detail(request, group_id):
    group = Groups.objects.get(id=group_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        student_id = request.POST.get('student_id')
        student = Students.objects.get(id=student_id)

        if action == 'add':
            # 🔻 Знаходимо всі групи, де є цей студент, і видаляємо його звідти
            all_groups = Groups.objects.filter(students=student)
            for g in all_groups:
                if student in g.students:
                    g.students.remove(student)
                    g.save()

            # 🔹 Додаємо студента в поточну групу (якщо ще не в ній)
            if student not in group.students:
                group.students.append(student)

            # 🔹 Оновлюємо поле group у студенті
            student.group = group
            student.save()
            group.save()

        elif action == 'remove':
            if student in group.students:
                group.students.remove(student)
                group.save()

            # 🔻 Очистити поле group у студенті (залишаючи поле)
            student.update(set__group=None)

        return redirect('group_detail', group_id=group.id)

    all_students = Students.objects.all()
    return render(request, 'admin_panel/group_detail.html', {
        'group': group,
        'students': group.students,
        'all_students': all_students,
    })

def admin_add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('name').strip()

        if group_name and not Groups.objects(name=group_name).first():
            group = Groups(name=group_name, students=[])
            group.save()
            return redirect('admin_groups')  # Повертає на список груп

    return render(request, 'admin_panel/add_group.html')

def admin_journal(request):
    journals = Journal.objects.all()
    return render(request, 'admin_panel/journals.html', {'journals': journals})


def admin_view_journal(request, journal_id):
    if request.session.get('role') != 'admin':
        return redirect('login')

    try:
        journal = Journal.objects.get(id=ObjectId(journal_id))
    except Journal.DoesNotExist:
        raise Http404("Журнал не знайдено")

    # Підготовка інформації про сесії
    sessions = []
    for i in range(len(journal.session_types)):
        sessions.append({
            'type': journal.session_types[i],
            'max_points': journal.max_points_per_session[i] if i < len(journal.max_points_per_session) else None,
            'deadline': journal.deadlines[i] if i < len(journal.deadlines) else None,
            'penalty': journal.late_penalties[i] if i < len(journal.late_penalties) else None,
        })

    # Підготовка інформації про студентів
    students = []
    for s in journal.students:
        session_data = []
        for i in range(len(s.grades)):
            session_data.append({
                'grade': s.grades[i],
                'comment': s.comments[i] if i < len(s.comments) else '',
                'max_point': journal.max_points_per_session[i] if i < len(journal.max_points_per_session) else '',
            })
        students.append({
            'name': s.name,
            'total': s.total,
            'session_data': session_data,
        })

    # Отримання імені викладача
    lecturer = None
    try:
        lecturer_obj = Lecturer.objects.get(id=journal.lecturer.id)
        lecturer = lecturer_obj.name
    except Lecturer.DoesNotExist:
        lecturer = "Невідомий викладач"

    students.sort(key=lambda x: x['name'].lower())

    return render(request, 'admin_panel/view_journal.html', {
        'journal': journal,
        'sessions': sessions,
        'students': students,
        'lecturer_name': lecturer,
    })