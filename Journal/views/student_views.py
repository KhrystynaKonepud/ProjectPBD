from django.shortcuts import render, redirect
from Journal.models.students import Students
from Journal.models.journal import Journal

def student_dashboard(request):
    student_id = request.session.get('user_id')
    if not student_id or request.session.get('role') != 'student':
        return redirect('login')

    student = Students.objects(id=student_id).first()

    # Ищем все журналы, в которых присутствует данный студент
    student_journals = Journal.objects.filter(students__student_id=student_id)

    return render(request, 'student_dashboard.html', {
        'student': student,
        'student_journals': student_journals,
    })