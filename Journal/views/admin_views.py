from django.shortcuts import render, redirect
from Journal.models.admin import Admin
from Journal.forms.profile_edit_form import AdminProfileForm
from django.contrib.auth.hashers import make_password

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
