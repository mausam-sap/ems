from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.decorators import admin_required
from apps.employees.models import Employee
from .models import PerformancePrediction, AbsenteeismPrediction
from .ml.predict import predict_performance, predict_absenteeism

@admin_required
def ai_dashboard(request):
    employees = Employee.objects.filter(is_active=True).select_related('user', 'department')
    return render(request, 'ai_engine/ai_dashboard.html', {'employees': employees})

@admin_required
def run_predictions(request):
    employees = Employee.objects.filter(is_active=True)
    count = 0
    for emp in employees:
        score, risk, att_rate = predict_performance(emp)
        if score is not None:
            PerformancePrediction.objects.create(
                employee=emp, predicted_score=score,
                risk_label=risk, attendance_rate=att_rate
            )
        prob, label = predict_absenteeism(emp)
        if prob is not None:
            AbsenteeismPrediction.objects.create(
                employee=emp, risk_probability=prob, risk_label=label
            )
        count += 1
    messages.success(request, f"Predictions generated for {count} employees.")
    return redirect('ai:dashboard')

@admin_required
def employee_prediction(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    perf = PerformancePrediction.objects.filter(employee=emp).first()
    absent = AbsenteeismPrediction.objects.filter(employee=emp).first()

    if not perf:
        score, risk, att_rate = predict_performance(emp)
        if score is not None:
            perf = PerformancePrediction.objects.create(
                employee=emp, predicted_score=score,
                risk_label=risk, attendance_rate=att_rate
            )
    if not absent:
        prob, label = predict_absenteeism(emp)
        if prob is not None:
            absent = AbsenteeismPrediction.objects.create(
                employee=emp, risk_probability=prob, risk_label=label
            )
    return render(request, 'ai_engine/employee_prediction.html', {
        'emp': emp, 'perf': perf, 'absent': absent
    })

@login_required
def my_prediction(request):
    emp = get_object_or_404(Employee, user=request.user)
    perf = PerformancePrediction.objects.filter(employee=emp).first()
    absent = AbsenteeismPrediction.objects.filter(employee=emp).first()
    if not perf:
        score, risk, att_rate = predict_performance(emp)
        if score is not None:
            perf = PerformancePrediction.objects.create(
                employee=emp, predicted_score=score,
                risk_label=risk, attendance_rate=att_rate
            )
    return render(request, 'ai_engine/my_prediction.html', {'emp': emp, 'perf': perf, 'absent': absent})
