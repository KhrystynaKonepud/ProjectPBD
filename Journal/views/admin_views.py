from django.shortcuts import render, redirect
from Journal.models.admin import Admin

def admin_dashboard(request):
    admin_id = request.session.get('user_id')
    if not admin_id or request.session.get('role') != 'admin':
        return redirect('login')

    admin = Admin.objects(id=admin_id).first()
    return render(request, 'admin_dashboard.html', {'admin': admin})
