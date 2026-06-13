import numpy as np
import joblib
from pathlib import Path
from datetime import date

MODELS_DIR = Path(__file__).resolve().parent.parent / 'ml_models'

def _load_model(name):
    path = MODELS_DIR / name
    if not path.exists():
        return None
    return joblib.load(path)

def _build_features(employee):
    from apps.attendance.models import Attendance
    from apps.leave.models import LeaveRequest

    today = date.today()
    last_90_days_start = date(today.year, today.month, 1)
    if today.month > 3:
        last_90_days_start = date(today.year, today.month - 3, 1)

    total_att = Attendance.objects.filter(employee=employee).count()
    present = Attendance.objects.filter(
        employee=employee, status__in=['Present', 'Late', 'Half-Day']
    ).count()
    absent = Attendance.objects.filter(employee=employee, status='Absent').count()
    late = Attendance.objects.filter(employee=employee, status='Late').count()
    attendance_rate = (present / total_att) if total_att > 0 else 0.8

    leave_days = sum(
        lr.days_count for lr in LeaveRequest.objects.filter(
            employee=employee, status='Approved', start_date__year=today.year
        )
    )

    tenure_months = max(1, (today - employee.joining_date).days // 30)

    # Derive delay from Late count: each Late record ~ 15 min avg delay
    check_in_delay = min((late / max(total_att, 1)) * 60, 90)

    return np.array([[attendance_rate, leave_days, tenure_months, check_in_delay]])

def predict_performance(employee):
    model = _load_model('performance_model.pkl')
    if model is None:
        return None, None, None
    features = _build_features(employee)
    raw = float(model.predict(features)[0])
    # Scale from model's effective range [45, 85] to full [0, 100]
    score = (raw - 45) / (85 - 45) * 100
    score = round(min(max(score, 0), 100), 2)
    risk = 'High' if score < 35 else 'Medium' if score < 65 else 'Low'
    att_rate = float(features[0][0])
    return score, risk, att_rate

def predict_absenteeism(employee):
    model = _load_model('absenteeism_model.pkl')
    if model is None:
        return None, None
    features = _build_features(employee)
    prob = float(model.predict_proba(features)[0][1])
    label = 'High' if prob > 0.6 else 'Medium' if prob > 0.3 else 'Low'
    return round(prob * 100, 1), label
