from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, ChangePasswordForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request,
                            username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def dashboard_redirect(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    return redirect('employee_dashboard')

@login_required
def change_password(request):
    form = ChangePasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = request.user
        if not user.check_password(form.cleaned_data['old_password']):
            messages.error(request, 'Current password is incorrect.')
        else:
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.success(request, 'Password changed. Please log in again.')
            return redirect('accounts:login')
    return render(request, 'accounts/change_password.html', {'form': form})
