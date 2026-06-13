from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from apps.accounts.decorators import admin_required
from apps.accounts.models import User
from .models import Employee, Department
from .forms import EmployeeForm, EmployeeUpdateForm, DepartmentForm

@login_required
def employee_list(request):
    if request.user.is_admin():
        employees = Employee.objects.select_related('user', 'department').all()
        dept_filter = request.GET.get('dept')
        search = request.GET.get('q')
        if dept_filter:
            employees = employees.filter(department_id=dept_filter)
        if search:
            employees = employees.filter(user__first_name__icontains=search) | \
                        employees.filter(user__last_name__icontains=search) | \
                        employees.filter(employee_id__icontains=search)
        paginator = Paginator(employees, 25)
        page = paginator.get_page(request.GET.get('page'))
        departments = Department.objects.all()
        return render(request, 'employees/employee_list.html', {
            'page_obj': page, 'departments': departments, 'search': search, 'dept_filter': dept_filter
        })
    # employee sees own profile
    emp = get_object_or_404(Employee, user=request.user)
    return redirect('employees:profile', pk=emp.pk)

@admin_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        emp_id = form.cleaned_data['employee_id']
        username = emp_id.lower()
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists.")
        else:
            user = User.objects.create_user(
                username=username,
                password='emp@123',
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data.get('email', ''),
                role='employee'
            )
            emp = form.save(commit=False)
            emp.user = user
            emp.save()
            messages.success(request, f"Employee created. Default password: emp@123")
            return redirect('employees:list')
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Employee'})

@admin_required
def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    initial = {
        'first_name': emp.user.first_name,
        'last_name': emp.user.last_name,
        'email': emp.user.email,
    }
    form = EmployeeUpdateForm(request.POST or None, instance=emp, initial=initial)
    if request.method == 'POST' and form.is_valid():
        emp.user.first_name = form.cleaned_data['first_name']
        emp.user.last_name = form.cleaned_data['last_name']
        emp.user.email = form.cleaned_data.get('email', '')
        emp.user.save()
        form.save()
        messages.success(request, "Employee updated.")
        return redirect('employees:list')
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Employee', 'emp': emp})

@admin_required
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp.user.delete()
        messages.success(request, "Employee deleted.")
        return redirect('employees:list')
    return render(request, 'employees/employee_confirm_delete.html', {'emp': emp})

@login_required
def employee_profile(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if not request.user.is_admin() and emp.user != request.user:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    return render(request, 'employees/employee_profile.html', {'emp': emp})

@admin_required
def department_list(request):
    depts = Department.objects.all()
    return render(request, 'employees/department_list.html', {'depts': depts})

@admin_required
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Department created.")
        return redirect('employees:departments')
    return render(request, 'employees/department_form.html', {'form': form})

@admin_required
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Department updated.")
        return redirect('employees:departments')
    return render(request, 'employees/department_form.html', {'form': form, 'dept': dept})

@admin_required
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, "Department deleted.")
        return redirect('employees:departments')
    return render(request, 'employees/department_confirm_delete.html', {'dept': dept})
