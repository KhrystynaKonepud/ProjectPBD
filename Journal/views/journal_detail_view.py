# from django.shortcuts import render, get_object_or_404
# from Journal.models.journal import Journal

# def journal_detail(request, journal_id):
#     journal = get_object_or_404(Journal, id=journal_id)

#     # Можно добавить другие данные, например, студентов, оценку и т.д.
#     return render(request, 'journal_detail.html', {
#         'journal': journal,
#     })
# from django.shortcuts import render
# from mongoengine import DoesNotExist
# from Journal.models.journal import Journal
# from django.http import Http404

# def journal_detail(request, journal_id):
#     try:
#         # Получаем объект журнала по его id
#         journal = Journal.objects.get(id=journal_id)
#     except DoesNotExist:
#         # Если объект не найден, возвращаем 404
#         raise Http404("Journal not found")

#     # Подготовка данных для передачи в шаблон
#     context = {
#         'journal': journal,
#         'lecturer': journal.lecturer,
#         'subject': journal.subject,
#         'group': journal.group,
#         'total_points': journal.total_points,
#         'session_types': journal.session_types,
#         'max_points_per_session': journal.max_points_per_session,
#         'deadlines': journal.deadlines,
#         'late_penalties': journal.late_penalties,
#         'comments_enabled': journal.comments_enabled,
#     }

#     # Выводим студентов и их данные (оценки, комментарии)
#     students_data = []
#     for student in journal.students:
#         student_data = {
#             'name': student.name,
#             'grades': student.grades,
#             'comments': student.comments,
#             'total': student.total
#         }
#         students_data.append(student_data)

#     context['students'] = students_data

#     return render(request, 'journal_detail.html', context)

# from django.shortcuts import render
# from mongoengine import DoesNotExist
# from Journal.models.journal import Journal
# from django.http import Http404

# def journal_detail(request, journal_id):
#     try:
#         # Получаем объект журнала по его id
#         journal = Journal.objects.get(id=journal_id)
#     except DoesNotExist:
#         # Если объект не найден, возвращаем 404
#         raise Http404("Journal not found")

#     # Подготовка данных для передачи в шаблон
#     context = {
#         'journal': journal,
#         'lecturer': journal.lecturer,
#         'subject': journal.subject,
#         'group': journal.group,
#         'total_points': journal.total_points,
#         'session_types': journal.session_types,
#         'max_points_per_session': journal.max_points_per_session,
#         'deadlines': journal.deadlines,
#         'late_penalties': journal.late_penalties,
#         'comments_enabled': journal.comments_enabled,
#     }

#     students_data = []
#     for student in journal.students:
#         student_data = {
#             'name': student.name,
#             'grades': student.grades,
#             'comments': student.comments,
#             'total': student.total
#         }
#         students_data.append(student_data)

#     context['students'] = students_data

#     return render(request, 'journal_detail.html', context)



from django.shortcuts import render
from mongoengine import DoesNotExist
from Journal.models.journal import Journal
from django.http import Http404

def journal_detail(request, journal_id):
    try:
        # Получаем объект журнала по его id
        journal = Journal.objects.get(id=journal_id)
    except DoesNotExist:
        # Если объект не найден, возвращаем 404
        raise Http404("Journal not found")

    # Склеиваем данные по индексам в один список словарей
    sessions_info = []
    for i in range(len(journal.session_types)):
        sessions_info.append({
            'type': journal.session_types[i],
            'max_points': journal.max_points_per_session[i],
            'deadline': journal.deadlines[i],
            'penalty': journal.late_penalties[i],
        })

    # Подготовка данных для передачи в шаблон
    context = {
        'journal': journal,
        'lecturer': journal.lecturer,
        'subject': journal.subject,
        'group': journal.group,
        'total_points': journal.total_points,
        'comments_enabled': journal.comments_enabled,
        'sessions_info': sessions_info,  # ✅ передаем сюда объединенные сессии
    }

    # Выводим студентов и их данные (оценки, комментарии)
    students_data = []
    for student in journal.students:
        student_data = {
            'name': student.name,
            'grades': student.grades,
            'comments': student.comments,
            'total': student.total
        }
        students_data.append(student_data)

    context['students'] = students_data

    return render(request, 'journal_detail.html', context)
