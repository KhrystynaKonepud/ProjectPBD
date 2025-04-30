from django.shortcuts import render, redirect
from Journal.models.lecturer import Lecturer
from Journal.models import Journal, JournalStudent, Groups, Students, Subjects
from Journal.forms.journal_form import JournalForm
from django.contrib import messages


def lecturer_dashboard(request):
    lecturer_id = request.session.get('user_id')
    if not lecturer_id or request.session.get('role') != 'lecturer':
        return redirect('login')

    lecturer = Lecturer.objects(id=lecturer_id).first()
    return render(request, 'lecturer_panel/lecturer_dashboard.html', {'lecturer': lecturer})


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




