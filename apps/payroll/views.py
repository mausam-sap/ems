import calendar as cal_module
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from apps.accounts.decorators import admin_required
from apps.employees.models import Employee
from .models import PayrollRecord
from .forms import GeneratePayrollForm
from .utils import calculate_payroll
from .pdf import generate_payslip_pdf

@admin_required
def payroll_list(request):
    month = int(request.GET.get('month', date.today().month))
    year = int(request.GET.get('year', date.today().year))
    records = PayrollRecord.objects.filter(month=month, year=year).select_related('employee__user')
    months = [(i, cal_module.month_name[i]) for i in range(1, 13)]
    years = list(range(date.today().year - 2, date.today().year + 1))
    return render(request, 'payroll/payroll_list.html', {
        'records': records, 'month': month, 'year': year,
        'months': months, 'years': years,
        'month_name': cal_module.month_name[month]
    })

@admin_required
def generate_payroll(request):
    form = GeneratePayrollForm(request.POST or None)
    preview = None
    if request.method == 'POST' and form.is_valid():
        emp = form.cleaned_data['employee']
        month = int(form.cleaned_data['month'])
        year = int(form.cleaned_data['year'])
        bonus = form.cleaned_data['bonus']
        data = calculate_payroll(emp, month, year)
        data['bonus'] = bonus
        data['net_salary'] = data['net_salary'] + bonus

        if 'confirm' in request.POST:
            pr, created = PayrollRecord.objects.update_or_create(
                employee=emp, month=month, year=year,
                defaults={
                    'basic_salary': data['basic_salary'],
                    'bonus': data['bonus'],
                    'deductions': data['deductions'],
                    'net_salary': data['net_salary'],
                    'working_days': data['working_days'],
                    'present_days': data['present_days'],
                }
            )
            msg = "Payroll generated." if created else "Payroll updated."
            messages.success(request, msg)
            return redirect('payroll:list')
        preview = {'emp': emp, 'month': month, 'year': year, **data}
    return render(request, 'payroll/generate_payroll.html', {'form': form, 'preview': preview})

@login_required
def payslip_detail(request, pk):
    pr = get_object_or_404(PayrollRecord, pk=pk)
    if not request.user.is_admin() and pr.employee.user != request.user:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    return render(request, 'payroll/payslip_detail.html', {'pr': pr})

@login_required
def payslip_pdf(request, pk):
    pr = get_object_or_404(PayrollRecord, pk=pk)
    if not request.user.is_admin() and pr.employee.user != request.user:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{pr.employee.employee_id}_{pr.month}_{pr.year}.pdf"'
    generate_payslip_pdf(response, pr)
    return response

@login_required
def my_payroll(request):
    emp = get_object_or_404(Employee, user=request.user)
    records = PayrollRecord.objects.filter(employee=emp)
    return render(request, 'payroll/my_payroll.html', {'records': records})
