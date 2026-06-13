# AI-Based Employee Management System

An intelligent HR management web application built with Python and Django, featuring Machine Learning-powered employee performance prediction and absenteeism risk analysis.

---

## Prerequisites

Before you begin, make sure the following software is installed on your Windows machine:

| Software | Version | Download |
| --- | --- | --- |
| Python | 3.9 or higher | [python.org/downloads](https://www.python.org/downloads/) |
| Git | Latest | [git-scm.com/download/win](https://git-scm.com/download/win) |
| Google Chrome or Firefox | Latest | For running the web app |

> **Important:** During Python installation, check **"Add Python to PATH"** before clicking Install.

To verify Python is installed correctly, open Command Prompt and run:

```cmd
python --version
```

You should see something like `Python 3.9.x` or higher.

---

## Setup Instructions

### Step 1 — Clone the Repository

Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter) and run:

```cmd
git clone https://github.com/mausam-sap/ems.git
cd ems
```

### Step 2 — Install Dependencies

```cmd
pip install -r requirements.txt
```

This will install all required packages including Django, scikit-learn, pandas, Plotly, ReportLab, and others. It may take a few minutes.

### Step 3 — Set Up the Database

```cmd
python manage.py migrate
```

### Step 4 — Train the AI Models

```cmd
python manage.py train_models
```

### Step 5 — Create an Admin Account

```cmd
python manage.py shell -c "from apps.accounts.models import User; User.objects.create_superuser('admin', 'admin@ems.com', 'admin@123', role='admin', first_name='System', last_name='Admin') if not User.objects.filter(username='admin').exists() else None"
```

This creates an admin account with username `admin` and password `admin@123`.

### Step 6 — (Optional) Load Sample Data

To populate the system with 20 sample employees, 6 months of attendance, leave records, and payroll data:

```cmd
python manage.py seed_data
```

### Step 7 — Run the Application

```cmd
python manage.py runserver
```

Open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Login Credentials

| Role | Username | Password |
| --- | --- | --- |
| Admin | `admin` | `admin@123` |
| Employee (sample) | `emp001` to `emp020` | `emp@123` |

> Employee usernames are the Employee ID in lowercase (e.g., `emp001`, `emp002`, ..., `emp020`). Only available after running `seed_data`.

---

## Project Structure

```text
ems/
├── apps/
│   ├── accounts/       # Authentication and role management
│   ├── employees/      # Employee and department CRUD
│   ├── attendance/     # Attendance tracking
│   ├── leave/          # Leave request workflow
│   ├── payroll/        # Salary calculation and PDF payslips
│   ├── ai_engine/      # ML models and predictions
│   └── reports/        # Dashboards and analytics
├── templates/          # HTML templates (Bootstrap 5)
├── static/             # Static files (CSS, JS)
├── ems/                # Django project settings and URLs
├── manage.py
├── requirements.txt
└── tests.py
```

---

## Features

- **Employee Management** — Add, edit, and manage employee records and departments
- **Attendance Tracking** — Daily and bulk attendance entry with monthly calendar view
- **Leave Management** — Online leave applications with admin approval workflow and balance tracking
- **Payroll** — Auto-calculated salaries with downloadable PDF payslips
- **AI Performance Prediction** — Random Forest model predicts employee performance scores (0–100)
- **Absenteeism Risk** — Logistic Regression model estimates future absenteeism probability
- **Analytics Dashboard** — Interactive Plotly charts for attendance trends, department analysis, and AI risk distribution
- **Role-Based Access** — Separate admin and employee portals

---

## Running Tests

```cmd
python -m pytest tests.py -v
```

All 5 unit tests should pass.

---

## Useful Commands

| Command | Description |
| --- | --- |
| `python manage.py runserver` | Start the development server |
| `python manage.py train_models` | Retrain AI models |
| `python manage.py seed_data` | Load dummy data |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py createsuperuser` | Create a new admin user |
| `python -m pytest tests.py -v` | Run automated tests |

---

## Troubleshooting

**`'python' is not recognized`**
→ Python is not added to PATH. Reinstall Python and check "Add Python to PATH" during setup.

**Port 8000 is already in use**
→ Run the server on a different port:

```cmd
python manage.py runserver 8080
```

Then visit [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3.9+ |
| Web Framework | Django 4.2 |
| Database | SQLite |
| Frontend | Bootstrap 5 + HTML |
| Charts | Plotly |
| Machine Learning | scikit-learn (Random Forest, Logistic Regression) |
| PDF Generation | ReportLab |
| Testing | pytest-django |

---

## License

This project is developed as an MCA Final Year Project for academic purposes.
