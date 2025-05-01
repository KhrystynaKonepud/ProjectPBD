from django.shortcuts import render
from mongoengine import DoesNotExist

from Journal.models import Lecturer
from Journal.models.journal import Journal
from django.http import Http404


def journal_detail(request, journal_id):
    try:
        journal = Journal.objects.get(id=journal_id)
    except DoesNotExist:
        raise Http404("Journal not found")


    # Підготовка інформації про сесії
    sessions = []
    for i in range(len(journal.session_types)):
        sessions.append({
            'type': journal.session_types[i],
            'max_points': journal.max_points_per_session[i] if i < len(journal.max_points_per_session) else None,
            'deadline': journal.deadlines[i] if i < len(journal.deadlines) else None,
            'penalty': journal.late_penalties[i] if i < len(journal.late_penalties) else None,
        })

    # Підготовка інформації про студентів з сортуванням за іменем
    students = []
    for s in sorted(journal.students, key=lambda x: x.name.lower()):  # сортування за іменем (без урахування регістру)
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

    return render(request, 'journal_detail.html', {
        'journal': journal,
        'sessions': sessions,
        'students': students,
        'lecturer_name': lecturer,
    })
