from django.shortcuts import render, redirect
from Journal.models.lecturer import Lecturer

def lecturer_dashboard(request):
    lecturer_id = request.session.get('user_id')
    if not lecturer_id or request.session.get('role') != 'lecturer':
        return redirect('login')

    lecturer = Lecturer.objects(id=lecturer_id).first()
    return render(request, 'lecturer_dashboard.html', {'lecturer': lecturer})
