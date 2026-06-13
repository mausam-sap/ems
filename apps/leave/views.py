from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.decorators import admin_required
from apps.employees.models import Employee
from .models import LeaveRequest
from .forms import LeaveRequestForm, LeaveReviewForm

def _get_leave_balance(emp):
    year = date.today().year
    approved = LeaveRequest.objects.filter(
        employee=emp, status='Approved', start_date__year=year
    )
    used = {lt: 0 for lt in ['Annual', 'Sick', 'Casual']}
    for lr in approved:
        used[lr.leave_type] = used.get(lr.leave_type, 0) + lr.days_count
    return {
        'Annual': {'limit': 12, 'used': used['Annual'], 'remaining': max(0, 12 - used['Annual'])},
        'Sick':   {'limit': 6,  'used': used['Sick'],   'remaining': max(0, 6 - used['Sick'])},
        'Casual': {'limit': 6,  'used': used['Casual'], 'remaining': max(0, 6 - used['Casual'])},
    }

@login_required
def leave_list(request):
    if request.user.is_admin():
        status_filter = request.GET.get('status', '')
        leaves = LeaveRequest.objects.select_related('employee__user').all()
        if status_filter:
            leaves = leaves.filter(status=status_filter)
        return render(request, 'leave/admin_leave_list.html', {'leaves': leaves, 'status_filter': status_filter})
    emp = get_object_or_404(Employee, user=request.user)
    leaves = LeaveRequest.objects.filter(employee=emp)
    balance = _get_leave_balance(emp)
    return render(request, 'leave/my_leaves.html', {'leaves': leaves, 'balance': balance})

@login_required
def leave_apply(request):
    emp = get_object_or_404(Employee, user=request.user)
    form = LeaveRequestForm(request.POST or None)
    balance = _get_leave_balance(emp)
    if request.method == 'POST' and form.is_valid():
        lr = form.save(commit=False)
        lr.employee = emp
        leave_type = lr.leave_type
        remaining = balance[leave_type]['remaining']
        if lr.days_count > remaining:
            messages.error(request, f"Not enough {leave_type} leave balance. Remaining: {remaining} days.")
        else:
            lr.save()
            messages.success(request, "Leave request submitted.")
            return redirect('leave:list')
    return render(request, 'leave/leave_form.html', {'form': form, 'balance': balance})

@admin_required
def leave_review(request, pk):
    lr = get_object_or_404(LeaveRequest, pk=pk)
    form = LeaveReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        lr.status = form.cleaned_data['status']
        lr.review_note = form.cleaned_data['review_note']
        lr.reviewed_by = request.user
        lr.save()
        messages.success(request, f"Leave request {lr.status.lower()}.")
        return redirect('leave:list')
    return render(request, 'leave/leave_review.html', {'lr': lr, 'form': form})

@login_required
def leave_cancel(request, pk):
    emp = get_object_or_404(Employee, user=request.user)
    lr = get_object_or_404(LeaveRequest, pk=pk, employee=emp, status='Pending')
    if request.method == 'POST':
        lr.delete()
        messages.success(request, "Leave request cancelled.")
    return redirect('leave:list')
