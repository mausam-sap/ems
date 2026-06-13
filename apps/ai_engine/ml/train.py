import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

MODELS_DIR = Path(__file__).resolve().parent.parent / 'ml_models'
MODELS_DIR.mkdir(exist_ok=True)

def _generate_seed_data(n=300):
    np.random.seed(42)
    attendance_rate = np.clip(np.random.normal(0.82, 0.15, n), 0.2, 1.0)
    leave_days = np.random.randint(0, 20, n)
    tenure_months = np.random.randint(1, 120, n)
    check_in_delay = np.clip(np.random.exponential(10, n), 0, 90)

    performance_score = (
        attendance_rate * 50
        + np.clip((tenure_months / 120) * 20, 0, 20)
        + np.clip((1 - check_in_delay / 90) * 15, 0, 15)
        + np.clip((1 - leave_days / 20) * 15, 0, 15)
        + np.random.normal(0, 3, n)
    )
    performance_score = np.clip(performance_score, 0, 100)

    absenteeism_risk = (attendance_rate < 0.7).astype(int)

    X = np.column_stack([attendance_rate, leave_days, tenure_months, check_in_delay])
    return X, performance_score, absenteeism_risk

def train_models():
    X, y_perf, y_absent = _generate_seed_data()

    perf_model = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    perf_model.fit(X, y_perf)
    joblib.dump(perf_model, MODELS_DIR / 'performance_model.pkl')

    absent_model = Pipeline([
        ('scaler', StandardScaler()),
        ('lr', LogisticRegression(random_state=42))
    ])
    absent_model.fit(X, y_absent)
    joblib.dump(absent_model, MODELS_DIR / 'absenteeism_model.pkl')

    print(f"Models trained and saved to {MODELS_DIR}")

if __name__ == '__main__':
    train_models()
