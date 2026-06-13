import calendar
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.decorators import admin_required
from apps.employees.models import Employee
from .models import Attendance
from .forms import AttendanceForm, BulkAttendanceForm

@admin_required
def attendance_list(request):
    selected_date = request.GET.get('date', date.today().isoformat())
    records = Attendance.objects.filter(date=selected_date).select_related('employee__user')
    return render(request, 'attendance/attendance_list.html', {
        'records': records, 'selected_date': selected_date
    })

@admin_required
def attendance_mark(request):
    form = AttendanceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        att, created = Attendance.objects.update_or_create(
            employee=form.cleaned_data['employee'],
            date=form.cleaned_data['date'],
            defaults={
                'status': form.cleaned_data['status'],
                'check_in': form.cleaned_data.get('check_in'),
                'check_out': form.cleaned_data.get('check_out'),
            }
        )
        messages.success(request, "Attendance recorded.")
        return redirect('attendance:list')
    return render(request, 'attendance/attendance_form.html', {'form': form})

@admin_required
def bulk_attendance(request):
    employees = Employee.objects.filter(is_active=True).select_related('user')
    form = BulkAttendanceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        att_date = form.cleaned_data['date']
        default_status = form.cleaned_data['default_status']
        for emp in employees:
            status = request.POST.get(f'status_{emp.pk}', default_status)
            Attendance.objects.update_or_create(
                employee=emp, date=att_date,
                defaults={'status': status}
            )
        messages.success(request, f"Attendance saved for {att_date}.")
        return redirect('attendance:list')
    return render(request, 'attendance/bulk_attendance.html', {
        'form': form, 'employees': employees,
        'status_choices': Attendance.STATUS_CHOICES
    })

@login_required
def my_attendance(request):
    emp = get_object_or_404(Employee, user=request.user)
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    records = Attendance.objects.filter(employee=emp, date__month=month, date__year=year)
    summary = {
        'present': records.filter(status='Present').count(),
        'absent': records.filter(status='Absent').count(),
        'half_day': records.filter(status='Half-Day').count(),
        'late': records.filter(status='Late').count(),
        'total': records.count(),
    }
    cal = calendar.monthcalendar(year, month)
    att_map = {r.date.day: r.status for r in records}
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    years = list(range(today.year - 2, today.year + 1))
    return render(request, 'attendance/my_attendance.html', {
        'emp': emp, 'summary': summary, 'cal': cal, 'att_map': att_map,
        'month': month, 'year': year, 'months': months, 'years': years,
        'month_name': calendar.month_name[month]
    })

@admin_required
def employee_attendance_report(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    records = Attendance.objects.filter(employee=emp, date__month=month, date__year=year)
    summary = {
        'present': records.filter(status='Present').count(),
        'absent': records.filter(status='Absent').count(),
        'half_day': records.filter(status='Half-Day').count(),
        'late': records.filter(status='Late').count(),
    }
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    years = list(range(today.year - 2, today.year + 1))
    return render(request, 'attendance/employee_attendance_report.html', {
        'emp': emp, 'records': records, 'summary': summary,
        'month': month, 'year': year, 'months': months, 'years': years,
        'month_name': calendar.month_name[month]
    })
