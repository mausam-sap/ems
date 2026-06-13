import calendar
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import admin_required
from apps.employees.models import Employee, Department
from apps.attendance.models import Attendance
from apps.leave.models import LeaveRequest
from apps.payroll.models import PayrollRecord
from apps.ai_engine.models import PerformancePrediction

def _chart_html(fig):
    return fig.to_html(full_html=False, include_plotlyjs=False)

@admin_required
def admin_dashboard(request):
    today = date.today()
    total_employees = Employee.objects.filter(is_active=True).count()
    total_departments = Department.objects.count()
    today_att = Attendance.objects.filter(date=today)
    today_present = today_att.filter(status__in=['Present', 'Late']).count()
    today_pct = round((today_present / total_employees * 100) if total_employees else 0, 1)
    pending_leaves = LeaveRequest.objects.filter(status='Pending').count()

    # Monthly attendance chart (last 6 months)
    months_labels, present_data, absent_data = [], [], []
    for i in range(5, -1, -1):
        m = today.month - i
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        atts = Attendance.objects.filter(date__month=m, date__year=y)
        p = atts.filter(status__in=['Present', 'Late', 'Half-Day']).count()
        a = atts.filter(status='Absent').count()
        months_labels.append(calendar.month_abbr[m])
        present_data.append(p)
        absent_data.append(a)

    att_fig = go.Figure(data=[
        go.Bar(name='Present', x=months_labels, y=present_data, marker_color='#198754'),
        go.Bar(name='Absent', x=months_labels, y=absent_data, marker_color='#dc3545'),
    ])
    att_fig.update_layout(barmode='group', height=300, margin=dict(l=20, r=20, t=30, b=20),
                          legend=dict(orientation='h'))
    att_chart = _chart_html(att_fig)

    # Department headcount pie
    dept_data = []
    for d in Department.objects.all():
        cnt = Employee.objects.filter(department=d, is_active=True).count()
        if cnt:
            dept_data.append((d.name, cnt))
    if dept_data:
        dept_fig = px.pie(names=[d[0] for d in dept_data], values=[d[1] for d in dept_data],
                          height=300)
        dept_fig.update_layout(margin=dict(l=0, r=0, t=20, b=0))
        dept_chart = _chart_html(dept_fig)
    else:
        dept_chart = None

    # AI risk distribution
    preds = PerformancePrediction.objects.values('risk_label')
    risk_counts = {'Low': 0, 'Medium': 0, 'High': 0}
    for p in preds:
        risk_counts[p['risk_label']] = risk_counts.get(p['risk_label'], 0) + 1
    risk_fig = px.bar(x=list(risk_counts.keys()), y=list(risk_counts.values()),
                      color=list(risk_counts.keys()),
                      color_discrete_map={'Low': '#198754', 'Medium': '#ffc107', 'High': '#dc3545'},
                      height=280, labels={'x': 'Risk', 'y': 'Count'})
    risk_fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
    risk_chart = _chart_html(risk_fig)

    recent_leaves = LeaveRequest.objects.filter(status='Pending').select_related('employee__user')[:5]
    recent_payrolls = PayrollRecord.objects.select_related('employee__user').order_by('-generated_on')[:5]

    return render(request, 'reports/admin_dashboard.html', {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'today_present': today_present,
        'today_pct': today_pct,
        'pending_leaves': pending_leaves,
        'att_chart': att_chart,
        'dept_chart': dept_chart,
        'risk_chart': risk_chart,
        'recent_leaves': recent_leaves,
        'recent_payrolls': recent_payrolls,
        'today': today,
    })

@login_required
def employee_dashboard(request):
    from apps.leave.views import _get_leave_balance
    emp = get_object_or_404(Employee, user=request.user)
    today = date.today()
    month_att = Attendance.objects.filter(employee=emp, date__month=today.month, date__year=today.year)
    att_summary = {
        'present': month_att.filter(status='Present').count(),
        'absent': month_att.filter(status='Absent').count(),
        'half_day': month_att.filter(status='Half-Day').count(),
        'late': month_att.filter(status='Late').count(),
    }
    balance = _get_leave_balance(emp)
    latest_payslip = PayrollRecord.objects.filter(employee=emp).first()
    from apps.ai_engine.models import PerformancePrediction
    perf = PerformancePrediction.objects.filter(employee=emp).first()
    pending_leaves = LeaveRequest.objects.filter(employee=emp, status='Pending').count()
    return render(request, 'reports/employee_dashboard.html', {
        'emp': emp, 'att_summary': att_summary, 'balance': balance,
        'latest_payslip': latest_payslip, 'perf': perf,
        'pending_leaves': pending_leaves, 'today': today,
        'month_name': calendar.month_name[today.month],
    })
