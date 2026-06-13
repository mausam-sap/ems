from decimal import Decimal
from apps.attendance.models import Attendance

def calculate_payroll(employee, month, year):
    working_days = 26
    attendance = Attendance.objects.filter(employee=employee, date__month=month, date__year=year)
    present_days = attendance.filter(status__in=['Present', 'Late']).count()
    half_days = attendance.filter(status='Half-Day').count()
    effective_days = present_days + (half_days * Decimal('0.5'))

    basic = employee.basic_salary
    if working_days > 0:
        per_day = basic / working_days
        deductions = per_day * (working_days - effective_days)
    else:
        deductions = Decimal('0')

    bonus = Decimal('0')
    net = basic + bonus - deductions
    return {
        'basic_salary': basic,
        'bonus': bonus,
        'deductions': round(deductions, 2),
        'net_salary': round(max(net, Decimal('0')), 2),
        'working_days': working_days,
        'present_days': int(present_days),
    }
