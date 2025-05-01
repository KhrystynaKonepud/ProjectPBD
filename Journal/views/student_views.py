from django.shortcuts import render, redirect
from Journal.models.students import Students

def student_dashboard(request):
    student_id = request.session.get('user_id')
    if not student_id or request.session.get('role') != 'student':
        return redirect('login')

    student = Students.objects(id=student_id).first()
    return render(request, 'student_dashboard.html', {'student': student})
