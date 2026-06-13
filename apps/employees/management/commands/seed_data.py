import random
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.accounts.models import User
from apps.employees.models import Department, Employee
from apps.attendance.models import Attendance
from apps.leave.models import LeaveRequest
from apps.payroll.models import PayrollRecord
from apps.payroll.utils import calculate_payroll

DEPARTMENTS = [
    ('Engineering', 'Software development and infrastructure'),
    ('Human Resources', 'Recruitment, onboarding, and employee welfare'),
    ('Finance', 'Accounting, budgeting, and financial reporting'),
    ('Marketing', 'Brand management, campaigns, and digital marketing'),
    ('Operations', 'Day-to-day business operations and logistics'),
    ('Sales', 'Client acquisition and revenue generation'),
]

EMPLOYEES = [
    ('Arjun',   'Sharma',   'Engineering',   'Senior Developer',    85000),
    ('Priya',   'Patel',    'Engineering',   'Frontend Developer',  72000),
    ('Rohit',   'Verma',    'Engineering',   'Backend Developer',   78000),
    ('Sneha',   'Singh',    'Engineering',   'QA Engineer',         65000),
    ('Karan',   'Mehta',    'Engineering',   'DevOps Engineer',     90000),
    ('Ananya',  'Gupta',    'Human Resources','HR Manager',         70000),
    ('Vikram',  'Joshi',    'Human Resources','HR Executive',       48000),
    ('Pooja',   'Nair',     'Finance',       'Finance Manager',     80000),
    ('Aditya',  'Kumar',    'Finance',       'Accountant',          55000),
    ('Neha',    'Reddy',    'Finance',       'Financial Analyst',   62000),
    ('Suresh',  'Iyer',     'Marketing',     'Marketing Manager',   75000),
    ('Divya',   'Menon',    'Marketing',     'Content Writer',      45000),
    ('Rahul',   'Bose',     'Marketing',     'SEO Specialist',      52000),
    ('Meera',   'Pillai',   'Operations',    'Operations Manager',  72000),
    ('Deepak',  'Rao',      'Operations',    'Logistics Coordinator',50000),
    ('Anjali',  'Chopra',   'Operations',    'Process Analyst',     58000),
    ('Rajesh',  'Tiwari',   'Sales',         'Sales Manager',       80000),
    ('Sunita',  'Mishra',   'Sales',         'Sales Executive',     42000),
    ('Amit',    'Shah',     'Sales',         'Business Developer',  60000),
    ('Kavya',   'Kulkarni', 'Engineering',   'ML Engineer',         95000),
]

LEAVE_REASONS = [
    'Family function', 'Medical appointment', 'Personal work',
    'Travel', 'Home renovation', 'Festival celebration',
    'Child school event', 'Health checkup',
]

class Command(BaseCommand):
    help = 'Seed the database with realistic dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding dummy data...')
        with transaction.atomic():
            self._create_departments()
            self._create_employees()
            self._create_attendance()
            self._create_leaves()
            self._create_payroll()
        self.stdout.write(self.style.SUCCESS(
            f'Done! Created {len(EMPLOYEES)} employees with 6 months of attendance, leave, and payroll data.'
        ))
        self.stdout.write('Login with any employee: username = employee_id (lowercase), password = emp@123')

    def _create_departments(self):
        for name, desc in DEPARTMENTS:
            Department.objects.get_or_create(name=name, defaults={'description': desc})
        self.stdout.write(f'  Departments: {Department.objects.count()}')

    def _create_employees(self):
        today = date.today()
        for i, (first, last, dept_name, designation, salary) in enumerate(EMPLOYEES, start=1):
            emp_id = f'EMP{i:03d}'
            username = emp_id.lower()
            if Employee.objects.filter(employee_id=emp_id).exists():
                continue
            dept = Department.objects.get(name=dept_name)
            joining = today - timedelta(days=random.randint(180, 1000))
            user = User.objects.create_user(
                username=username, password='emp@123',
                first_name=first, last_name=last,
                email=f'{first.lower()}.{last.lower()}@company.com',
                role='employee'
            )
            Employee.objects.create(
                user=user, employee_id=emp_id,
                address=f'{random.randint(1,200)}, Sample Street, Mumbai',
                contact=f'9{random.randint(100000000, 999999999)}',
                department=dept, designation=designation,
                basic_salary=Decimal(salary),
                joining_date=joining,
            )
        self.stdout.write(f'  Employees: {Employee.objects.count()}')

    def _create_attendance(self):
        today = date.today()
        employees = Employee.objects.all()
        created = 0
        for emp in employees:
            # Seed 6 months of attendance
            for days_ago in range(180, 0, -1):
                att_date = today - timedelta(days=days_ago)
                if att_date.weekday() >= 5:  # skip weekends
                    continue
                if Attendance.objects.filter(employee=emp, date=att_date).exists():
                    continue
                # Vary attendance quality per employee
                rand = random.random()
                is_poor_attender = emp.pk % 5 == 0  # every 5th employee has poor attendance
                if is_poor_attender:
                    if rand < 0.20:
                        status = 'Absent'
                    elif rand < 0.30:
                        status = 'Half-Day'
                    elif rand < 0.45:
                        status = 'Late'
                    else:
                        status = 'Present'
                else:
                    if rand < 0.05:
                        status = 'Absent'
                    elif rand < 0.10:
                        status = 'Half-Day'
                    elif rand < 0.18:
                        status = 'Late'
                    else:
                        status = 'Present'
                Attendance.objects.create(employee=emp, date=att_date, status=status)
                created += 1
        self.stdout.write(f'  Attendance records: {created}')

    def _create_leaves(self):
        today = date.today()
        employees = Employee.objects.all()
        created = 0
        leave_types = ['Annual', 'Sick', 'Casual']
        statuses = ['Approved', 'Approved', 'Approved', 'Rejected', 'Pending']
        for emp in employees:
            num_leaves = random.randint(2, 5)
            for _ in range(num_leaves):
                days_ago = random.randint(10, 150)
                start = today - timedelta(days=days_ago)
                duration = random.randint(1, 3)
                end = start + timedelta(days=duration - 1)
                if end >= today:
                    continue
                if LeaveRequest.objects.filter(employee=emp, start_date=start).exists():
                    continue
                status = random.choice(statuses)
                LeaveRequest.objects.create(
                    employee=emp,
                    leave_type=random.choice(leave_types),
                    start_date=start, end_date=end,
                    reason=random.choice(LEAVE_REASONS),
                    status=status,
                )
                created += 1
        self.stdout.write(f'  Leave requests: {created}')

    def _create_payroll(self):
        today = date.today()
        employees = Employee.objects.all()
        created = 0
        for emp in employees:
            for months_ago in range(5, 0, -1):
                m = today.month - months_ago
                y = today.year
                while m <= 0:
                    m += 12
                    y -= 1
                if PayrollRecord.objects.filter(employee=emp, month=m, year=y).exists():
                    continue
                data = calculate_payroll(emp, m, y)
                bonus = Decimal(random.choice([0, 0, 0, 2000, 5000]))
                data['bonus'] = bonus
                data['net_salary'] = data['net_salary'] + bonus
                PayrollRecord.objects.create(
                    employee=emp, month=m, year=y,
                    basic_salary=data['basic_salary'],
                    bonus=data['bonus'],
                    deductions=data['deductions'],
                    net_salary=data['net_salary'],
                    working_days=data['working_days'],
                    present_days=data['present_days'],
                )
                created += 1
        self.stdout.write(f'  Payroll records: {created}')
