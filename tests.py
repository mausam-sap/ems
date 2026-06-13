import pytest
from decimal import Decimal

@pytest.mark.django_db
def test_create_employee_and_login(client):
    from apps.accounts.models import User
    from apps.employees.models import Department, Employee
    import datetime

    dept = Department.objects.create(name='Engineering')
    user = User.objects.create_user('emp001', password='test123', role='employee', first_name='Test', last_name='User')
    emp = Employee.objects.create(
        user=user, employee_id='EMP001', contact='9999999999',
        department=dept, designation='Developer',
        basic_salary=Decimal('50000'), joining_date=datetime.date(2023, 1, 1)
    )
    assert emp.full_name == 'Test User'
    assert user.is_admin() is False

    resp = client.post('/accounts/login/', {'username': 'emp001', 'password': 'test123'})
    assert resp.status_code == 302

@pytest.mark.django_db
def test_salary_calculation():
    from apps.accounts.models import User
    from apps.employees.models import Department, Employee
    from apps.attendance.models import Attendance
    from apps.payroll.utils import calculate_payroll
    import datetime

    dept = Department.objects.create(name='HR')
    user = User.objects.create_user('emp002', password='x', role='employee', first_name='Jane', last_name='Doe')
    emp = Employee.objects.create(
        user=user, employee_id='EMP002', contact='8888888888',
        department=dept, designation='Manager',
        basic_salary=Decimal('52000'), joining_date=datetime.date(2022, 6, 1)
    )
    # 20 present out of 26 working days
    for day in range(1, 21):
        Attendance.objects.create(employee=emp, date=datetime.date(2024, 1, day), status='Present')
    result = calculate_payroll(emp, 1, 2024)
    assert result['present_days'] == 20
    assert result['net_salary'] < Decimal('52000')
    assert result['net_salary'] > 0

@pytest.mark.django_db
def test_leave_balance():
    from apps.accounts.models import User
    from apps.employees.models import Department, Employee
    from apps.leave.models import LeaveRequest
    from apps.leave.views import _get_leave_balance
    import datetime

    dept = Department.objects.create(name='Ops')
    user = User.objects.create_user('emp003', password='x', role='employee', first_name='Bob', last_name='Smith')
    emp = Employee.objects.create(
        user=user, employee_id='EMP003', contact='7777777777',
        department=dept, designation='Analyst',
        basic_salary=Decimal('40000'), joining_date=datetime.date(2023, 3, 1)
    )
    LeaveRequest.objects.create(
        employee=emp, leave_type='Annual',
        start_date=datetime.date(2026, 3, 1), end_date=datetime.date(2026, 3, 5),
        reason='Vacation', status='Approved'
    )
    balance = _get_leave_balance(emp)
    assert balance['Annual']['used'] == 5
    assert balance['Annual']['remaining'] == 7

@pytest.mark.django_db
def test_admin_role_required(client):
    from apps.accounts.models import User
    user = User.objects.create_user('emptest', password='test', role='employee')
    client.login(username='emptest', password='test')
    resp = client.get('/employees/add/')
    assert resp.status_code == 302  # redirected, not allowed

def test_performance_prediction():
    import numpy as np
    from apps.ai_engine.ml.train import _generate_seed_data
    X, y_perf, y_absent = _generate_seed_data(50)
    assert X.shape == (50, 4)
    assert all(0 <= s <= 100 for s in y_perf)
    assert set(y_absent).issubset({0, 1})
