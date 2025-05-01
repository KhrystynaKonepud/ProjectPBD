from django.shortcuts import render, redirect
from Journal.models.lecturer import Lecturer
from Journal.models import Journal, JournalStudent, Groups, Students, Subjects
from Journal.forms.journal_form import JournalForm
from django.contrib import messages
from django.http import Http404
from bson import ObjectId
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from datetime import datetime


def lecturer_dashboard(request):
    lecturer_id = request.session.get('user_id')
    if not lecturer_id or request.session.get('role') != 'lecturer':
        return redirect('login')

    lecturer = Lecturer.objects(id=lecturer_id).first()
    journals = Journal.objects(lecturer=lecturer)
    return render(request, 'lecturer_panel/lecturer_dashboard.html', {
        'lecturer': lecturer,
        'journals': journals
    })


def create_journal(request):
    lecturer_id = request.session.get('user_id')
    if not lecturer_id or request.session.get('role') != 'lecturer':
        return redirect('login')

    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            try:
                group_name   = form.cleaned_data['group']
                subject_name = form.cleaned_data['subject']

                group    = Groups.objects.get(name=group_name)
                subject  = Subjects.objects.get(name=subject_name)
                lecturer = Lecturer.objects.get(id=lecturer_id)

                journal_students = []
                for student in Students.objects(group=group):
                    journal_students.append(JournalStudent(
                        student_id=student,
                        name=student.name,
                        grades=[0] * len(form.cleaned_data['session_types']),
                        comments=[""] * len(form.cleaned_data['session_types']),
                        total=0
                    ))

                j = Journal(
                    lecturer=lecturer,
                    subject=subject,
                    group=group,
                    total_points=form.cleaned_data['total_points'],
                    session_types=form.cleaned_data['session_types'],
                    max_points_per_session=form.cleaned_data['max_points_per_session'],
                    deadlines=form.cleaned_data['deadlines'],
                    late_penalties=form.cleaned_data['late_penalties'],
                    comments_enabled=form.cleaned_data['comments_enabled'],
                    students=journal_students
                )
                j.save()
                messages.success(request, "Журнал успішно створено!")
                return redirect('lecturer_dashboard')

            except Groups.DoesNotExist:
                form.add_error('group', "Такої групи не існує")
            except Subjects.DoesNotExist:
                form.add_error('subject', "Такого предмету не існує")
            except Lecturer.DoesNotExist:
                messages.error(request, "Викладача не знайдено. Спробуйте увійти ще раз.")
                return redirect('login')
    else:
        form = JournalForm()

    return render(request, 'lecturer_panel/create_journal.html', {'form': form})


def list_journals(request):
    """Список всіх журналів поточного викладача."""
    lecturer_id = request.session.get('user_id')
    if not lecturer_id or request.session.get('role') != 'lecturer':
        return redirect('login')

    lecturer = Lecturer.objects(id=lecturer_id).first()
    journals = Journal.objects(lecturer=lecturer)

    return render(request, 'lecturer_panel/lecturer_dashboard.html', {
        'lecturer': lecturer,
        'journals': journals,
    })


@csrf_protect
def view_journal(request, journal_id):
    lecturer_id = request.session.get('user_id')
    if not lecturer_id or request.session.get('role') != 'lecturer':
        return redirect('login')

    lecturer = Lecturer.objects(id=lecturer_id).first()
    if not lecturer:
        return redirect('login')

    try:
        journal = Journal.objects.get(id=ObjectId(journal_id), lecturer=lecturer)
    except Journal.DoesNotExist:
        raise Http404("Журнал не знайдено або у вас немає до нього доступу.")

    if request.method == 'POST':
        for i, student in enumerate(journal.students):
            total = 0
            for j in range(len(journal.session_types)):
                grade_key = f'student_{i}_grade_{j}'
                date_key = f'student_{i}_grade_{j}_date'
                comment_key = f'student_{i}_comment_{j}'

                grade_str = request.POST.get(grade_key, "0")
                date_str = request.POST.get(date_key, "")
                penalty = journal.late_penalties[j] if j < len(journal.late_penalties) else 0
                deadline = journal.deadlines[j] if j < len(journal.deadlines) else None

                try:
                    grade = int(grade_str)
                except ValueError:
                    grade = 0

                try:
                    submitted_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    submitted_date = None

                if deadline and submitted_date and submitted_date > deadline:
                    grade -= int(penalty)
                    grade = max(0, grade)

                student.grades[j] = grade

                if journal.comments_enabled and j < len(student.comments):
                    student.comments[j] = request.POST.get(comment_key, "")

                total += grade

            student.total = total

        journal.save()
        messages.success(request, "Зміни успішно збережено!")
        return redirect('view_journal', journal_id=journal_id)

    sessions = []
    for i in range(len(journal.session_types)):
        sessions.append({
            'type': journal.session_types[i],
            'max_points': journal.max_points_per_session[i] if i < len(journal.max_points_per_session) else None,
            'deadline': journal.deadlines[i] if i < len(journal.deadlines) else None,
            'penalty': journal.late_penalties[i] if i < len(journal.late_penalties) else None,
        })

    students = []
    for idx, s in enumerate(journal.students):
        session_data = []
        for i in range(len(s.grades)):
            session_data.append({
                'grade': s.grades[i],
                'comment': s.comments[i] if i < len(s.comments) else '',
                'max_point': journal.max_points_per_session[i] if i < len(journal.max_points_per_session) else '',
                'grade_name': f'student_{idx}_grade_{i}',
                'comment_name': f'student_{idx}_comment_{i}',
                'date_name': f'student_{idx}_grade_{i}_date',
            })
        students.append({
            'name': s.name,
            'total': s.total,
            'session_data': session_data,
        })

    students.sort(key=lambda x: x['name'].lower())

    return render(request, 'lecturer_panel/view_journal.html', {
        'journal': journal,
        'sessions': sessions,
        'students': students,
    })


@require_POST
def delete_journal(request, journal_id):
    lecturer_id = request.session.get('user_id')
    if not lecturer_id or request.session.get('role') != 'lecturer':
        return redirect('login')

    try:
        journal = Journal.objects.get(id=ObjectId(journal_id), lecturer=lecturer_id)
        journal.delete()
        messages.success(request, "Журнал успішно видалено.")
    except Journal.DoesNotExist:
        messages.error(request, "Журнал не знайдено або у вас немає прав на його видалення.")

    return redirect('lecturer_dashboard')