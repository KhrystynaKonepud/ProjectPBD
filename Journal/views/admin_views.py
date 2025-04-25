from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def admin_users(request):
    return render(request, 'admin_users.html')

def admin_groups(request):
    return render(request, 'admin_groups.html')

def admin_journals(request):
    return render(request, 'admin_journals.html')

def admin_subjects(request):
    return render(request, 'admin_subjects.html')

def admin_profile(request):
    return render(request, 'admin_panel/profile.html')  # ← нова view-функція
