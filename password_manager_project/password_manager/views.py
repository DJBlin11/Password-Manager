from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .forms import PasswordForm
from .models import Password

@login_required
def password_list(request):
    passwords = Password.objects.filter(user=request.user)
    return render(request, 'password_manager/password_list.html', {'passwords': passwords})

@login_required
def add_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.save(commit=False)
            password.user = request.user
            password.save()
            return redirect('password_list')
    else:
        form = PasswordForm()
    return render(request, 'password_manager/add_password.html', {'form': form})

# Обработка ошибки PermissionDenied
@permission_required('password_manager.view_password', raise_exception=True)
def permission_denied(request, exception):
    return render(request, 'password_manager/403.html', status=403)
